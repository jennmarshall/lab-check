import sqlite3 as sql

def connect(db):
    try:
        db = sql.connect(db)
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

# method to run SQL files
def run(file):
    db = connect('database.db')
    for statement in open(file).read().split(';'):
        if statement.strip():
            execute(db, statement)
    disconnect(db)

def create_borrower(db, borrower):
    create_borrower_statement = f'''INSERT INTO borrower (name, number, email)
        VALUES ('{borrower.name}', '{borrower.number}', '{borrower.email}');'''
    execute(db, create_borrower_statement)
    return db.cursor().lastrowid

def create_equipment(db, equipment):
    create_item_statement = f'''INSERT INTO equipment (name, category, dateBorrowed, laboratory, status, borrower)
        VALUES ('{equipment.name}', '{equipment.category}', '{equipment.dateBorrowed}', '{equipment.laboratory}', '{equipment.status}', '{equipment.borrower}');'''
    execute(db, create_item_statement)
    return db.cursor().lastrowid

def update_borrower(db, id, borrower):
    update_borrower_statement = f'''UPDATE borrower SET name = '{borrower.name}', number = '{borrower.number}', email = '{borrower.email}' WHERE id = {id};'''
    execute(db, update_borrower_statement)

def update_equipment(db, id, equipment):
    update_item_statement = f'''UPDATE equipment SET name = '{equipment.name}', category = '{equipment.category}', dateBorrowed = '{equipment.dateBorrowed}', laboratory = '{equipment.laboratory}', status = '{equipment.status}', borrower = '{equipment.borrower}' WHERE id = {id};'''
    execute(db, update_item_statement)

def read(db, select, table, where):
    read_statement = f'''SELECT {select} FROM {table} WHERE {where};'''
    cs = db.cursor()
    cs.execute(read_statement)
    return cs.fetchall()

def delete_borrower(db, table, id):
    delete_statement = f'''DELETE FROM {table} WHERE id = {id};'''
    execute(db, delete_statement)