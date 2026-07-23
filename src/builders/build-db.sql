CREATE TABLE IF NOT EXISTS borrower (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        number TEXT NOT NULL,
        email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        dateBorrowed TEXT NOT NULL,
        laboratory TEXT NOT NULL,
        status TEXT NOT NULL,
        borrower INTEGER NOT NULL,
        FOREIGN KEY (borrower) REFERENCES borrower(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);