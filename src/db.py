import sqlite3 as sql

def connect():
    try:
        db = sql.connect('database.db')
        print(f"INFO: Opened SQLite database with version {sql.sqlite_version} successfully.")
        return db
    except sql.OperationalError as e:
        print(f"ERROR: Failed to open database: {e}")

def disconnect(db):
    try:
        db.close()
        print(f"INFO: Database connection closed successfully.")
    except sql.OperationalError as e:
        print(f"ERROR: Failed to close database: {e}")

def execute(db, statement):
    try:
        cs = db.cursor()
        cs.execute(statement)
        db.commit()
        print(f"INFO: SQL statement executed successfully.")
    except sql.OperationalError as e:
        print(f"ERROR: Failed to execute SQL statement: {e}")

def build(file):
    db = connect()
    for statement in open(file).read().split(';'):
        if statement.strip():
            execute(db, statement)
    disconnect(db)