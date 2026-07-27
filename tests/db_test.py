import sqlite3 as sql
from types import SimpleNamespace

import pytest

import database as db


SCHEMA = """
CREATE TABLE borrower (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    number TEXT,
    email TEXT
);

CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    dateBorrowed TEXT,
    laboratory TEXT,
    status TEXT,
    borrower TEXT
);
"""


@pytest.fixture
def db_conn():
    """A fresh in-memory SQLite connection with the app schema loaded."""
    conn = sql.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.commit()
    yield conn
    conn.close()


def make_borrower(name="Jane Doe", number="123-456-7890",
                  email="jane@example.com"):
    return SimpleNamespace(name=name, number=number, email=email)


# Looks up a row's id directly as we cannot trust create_borrower and
# create_equipment
def get_id_by_name(conn, table, name):
    row = conn.execute(f"SELECT id FROM {table} WHERE name = ?",
                       (name,)).fetchone()
    return row[0]


def make_equipment(
    name="Microscope",
    category="Optics",
    dateBorrowed="2026-07-01",
    laboratory="Lab A",
    status="borrowed",
    borrower="1",
):
    return SimpleNamespace(
        name=name,
        category=category,
        dateBorrowed=dateBorrowed,
        laboratory=laboratory,
        status=status,
        borrower=borrower,
    )


# Testing connect and disconnect functionality
class TestConnectDisconnect:
    def test_connect_returns_usable_connection(self):
        conn = db.connect(":memory:")
        assert conn is not None
        assert isinstance(conn, sql.Connection)
        conn.close()

    def test_disconnect_closes_connection(self, db_conn):
        db.disconnect(db_conn)
        # Using a closed connection should raise ProgrammingError.
        with pytest.raises(sql.ProgrammingError):
            db_conn.execute("SELECT 1")

    def test_disconnect_on_already_closed_connection_does_not_raise(self,
                                                                    db_conn):
        db_conn.close()
        # disconnect() only catches OperationalError, and closing an
        # already-closed connection is actually a no-op in sqlite3,
        # so this should be silent rather than raising.
        db.disconnect(db_conn)


# Testing the execute functionality
class TestExecute:
    def test_execute_runs_and_commits_statement(self, db_conn):
        db.execute(db_conn, "INSERT INTO borrower (name, number, email) "
                            "VALUES ('Sam', '111', 's@example.com')")
        rows = db_conn.execute("SELECT name FROM borrower").fetchall()
        assert rows == [("Sam",)]

    def test_execute_swallows_operational_error(self, db_conn, capsys):
        # The incorrectly formed SQL raises sql.OperationalError, which
        # execute() catches and reports via print() instead of fullfilling.
        db.execute(db_conn, "INSERT INTO nonexistent_table VALUES (1)")
        captured = capsys.readouterr()
        assert "ERROR" in captured.out

    def test_execute_does_not_catch_integrity_error(self, db_conn):
        # borrower.name is NOT NULL, so this violates a constraint via
        # IntegrityError. A subclass execute() does NOT catch, since
        # it only excepts sql.OperationalError. This documents a real
        # gap, such errors will propagate and crash the caller.
        with pytest.raises(sql.IntegrityError):
            db.execute(db_conn, "INSERT INTO borrower (name) VALUES (NULL)")


# Testing creation functionality
class TestCreateBorrower:
    def test_create_borrower_inserts_row(self, db_conn):
        borrower = make_borrower(name="Alice", number="555-0100",
                                 email="alice@example.com")
        db.create_borrower(db_conn, borrower)

        row = db_conn.execute(
            "SELECT name, number, email FROM borrower WHERE name = 'Alice'"
        ).fetchone()
        assert row == ("Alice", "555-0100", "alice@example.com")

    def test_create_borrower_return_value_is_broken(self, db_conn):
        # TODO(bug): create_borrower() returns db.cursor().lastrowid, but
        # db.cursor() opens a brand-new cursor that never ran the
        # INSERT, so .lastrowid on it is always None. The row IS
        # correctly inserted, only the returned id is wrong. This
        # test documents current (broken) behavior; if the bug is
        # fixed to return the real id, this test should be updated.
        result = db.create_borrower(db_conn, make_borrower(name="Whoever"))
        assert result is None
        assert get_id_by_name(db_conn, "borrower", "Whoever") is not None

    def test_create_borrower_with_apostrophe_in_name_breaks(self, db_conn,
                                                            capsys):
        # database.py builds INSERT statements with f-strings, so a
        # name containing a single quote will corrupt the SQL
        # instead of being safely escaped, creating an SQL-injection or
        # correctness bug. execute() swallows the resulting
        # OperationalError and just prints it, so we assert on that
        # printed error and confirm the row was never inserted.
        db.create_borrower(db_conn, make_borrower(name="O'Brien"))

        captured = capsys.readouterr()
        assert "ERROR" in captured.out

        rows = db_conn.execute("SELECT * FROM borrower").fetchall()
        assert rows == []


class TestCreateEquipment:
    def test_create_equipment_inserts_row(self, db_conn):
        equipment = make_equipment(name="Oscilloscope", category="Electronics")
        db.create_equipment(db_conn, equipment)

        row = db_conn.execute(
            "SELECT name, category FROM equipment WHERE name = 'Oscilloscope'"
        ).fetchone()
        assert row == ("Oscilloscope", "Electronics")

    def test_create_equipment_return_value_is_broken(self, db_conn):
        # Same lastrowid bug as create_borrower(). See comment on
        # test_create_borrower_return_value_is_broken above.
        result = db.create_equipment(db_conn, make_equipment(name="Caliper"))
        assert result is None
        assert get_id_by_name(db_conn, "equipment", "Caliper") is not None


# Testing update functionality
class TestUpdateBorrower:
    def test_update_borrower_changes_fields(self, db_conn):
        db.create_borrower(db_conn, make_borrower(name="Old Name"))
        borrower_id = get_id_by_name(db_conn, "borrower", "Old Name")
        updated = make_borrower(name="New Name", number="999",
                                email="new@example.com")

        db.update_borrower(db_conn, borrower_id, updated)

        row = db_conn.execute(
            "SELECT name, number, email FROM borrower WHERE id = ?",
            (borrower_id,)
        ).fetchone()
        assert row == ("New Name", "999", "new@example.com")

    def test_update_borrower_with_nonexistent_id_is_a_no_op(self, db_conn):
        db.create_borrower(db_conn, make_borrower(name="Untouched"))
        db.update_borrower(db_conn, 9999, make_borrower(name="Ghost"))

        names = [r[0] for r in db_conn.execute("SELECT name FROM borrower"
                                               ).fetchall()]
        assert names == ["Untouched"]


class TestUpdateEquipment:
    def test_update_equipment_changes_fields(self, db_conn):
        db.create_equipment(db_conn, make_equipment(name="Centrifuge",
                                                    status="available"))
        eq_id = get_id_by_name(db_conn, "equipment", "Centrifuge")
        updated = make_equipment(status="borrowed", laboratory="Lab B")

        db.update_equipment(db_conn, eq_id, updated)

        row = db_conn.execute(
            "SELECT status, laboratory FROM equipment WHERE id = ?", (eq_id,)
        ).fetchone()
        assert row == ("borrowed", "Lab B")


# Test read functionality
class TestRead:
    def test_read_returns_matching_rows(self, db_conn):
        db.create_borrower(db_conn, make_borrower(name="Match",
                                                  email="match@example.com"))
        db.create_borrower(db_conn, make_borrower(name="Other",
                                                  email="other@example.com"))

        rows = db.read(db_conn, "name", "borrower", "name = 'Match'")
        assert rows == [("Match",)]

    def test_read_with_always_true_where_returns_all_rows(self, db_conn):
        db.create_borrower(db_conn, make_borrower(name="A"))
        db.create_borrower(db_conn, make_borrower(name="B"))

        rows = db.read(db_conn, "name", "borrower", "1=1")
        assert sorted(r[0] for r in rows) == ["A", "B"]

    def test_read_returns_empty_list_when_no_matches(self, db_conn):
        rows = db.read(db_conn, "*", "borrower", "1=0")
        assert rows == []


# Testing delete functionality
class TestDeleteBorrower:
    def test_delete_borrower_removes_row(self, db_conn):
        db.create_borrower(db_conn, make_borrower(name="ToDelete"))
        borrower_id = get_id_by_name(db_conn, "borrower", "ToDelete")

        db.delete_borrower(db_conn, "borrower", borrower_id)

        rows = db_conn.execute("SELECT * FROM borrower WHERE id = ?",
                               (borrower_id,)).fetchall()
        assert rows == []

    def test_delete_borrower_only_removes_matching_id(self, db_conn):
        db.create_borrower(db_conn, make_borrower(name="Keep"))
        db.create_borrower(db_conn, make_borrower(name="Delete"))
        delete_id = get_id_by_name(db_conn, "borrower", "Delete")

        db.delete_borrower(db_conn, "borrower", delete_id)

        remaining = [r[0] for r in db_conn.execute("SELECT name FROM borrower"
                                                   ).fetchall()]
        assert remaining == ["Keep"]

    def test_delete_borrower_works_on_equipment_table_too(self, db_conn):
        # delete_borrower() takes table as a parameter, so despite its
        # name it works generically against any table. Confirming
        # that behavior here since it's a bit of a misleading name.
        db.create_equipment(db_conn, make_equipment(name="Spectrometer"))
        eq_id = get_id_by_name(db_conn, "equipment", "Spectrometer")

        db.delete_borrower(db_conn, "equipment", eq_id)

        rows = db_conn.execute("SELECT * FROM equipment WHERE id = ?",
                               (eq_id,)).fetchall()
        assert rows == []


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
