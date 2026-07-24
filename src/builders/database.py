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


# def create_borrower(db, borrower):
#     create_borrower_statement = f'''INSERT INTO borower (name, number, email)
#         VALUES ('{borrower.name}', '{borrower.number}', '{borrower.email}');'''
#     execute(db, create_borrower_statement)

# def create_equipment(db, equipment):
#     create_item_statement = f'''INSERT INTO equipment (name, category, dateBorrowed, laboratory, status, borrower)
#         VALUES ('{equipment.name}', '{equipment.category}', '{equipment.dateBorrowed}', '{equipment.laboratory}', '{equipment.status}', '{equipment.borrower}');'''
#     execute(db, create_item_statement)

# def read_borrower(db, borrower):
#     read_borrower_statement = f'''SELECT * FROM borowers WHERE id = {borrower.id};'''
#     execute(db, read_borrower_statement)

# def read_equipment(db, equipment):
#     read_item_statement = f'''SELECT * FROM equipment WHERE id = {equipment.id};'''
#     execute(db, read_item_statement)

# def update_borrower(db, borrower):
#     update_borrower_statement = f'''UPDATE borowers SET name = '{borrower.name}', number = '{borrower.number}', email = '{borrower.email}' WHERE id = {borrower.id};'''
#     execute(db, update_borrower_statement)

# def update_equipment(db, equipment):
#     update_item_statement = f'''UPDATE equipment SET name = '{equipment.name}', category = '{equipment.category}', dateBorrowed = '{equipment.dateBorrowed}', laboratory = '{equipment.laboratory}', status = '{equipment.status}', borrower = '{equipment.borrower}' WHERE id = {equipment.id};'''
#     execute(db, update_item_statement)

# def delete_borrower(db, borrower):
#     delete_borrower_statement = f'''DELETE FROM borowers WHERE id = {borrower.id};'''
#     execute(db, delete_borrower_statement)

# def delete_equipment(db, equipment):
#     delete_item_statement = f'''DELETE FROM equipment WHERE id = {equipment.id};'''
#     execute(db, delete_item_statement)

# method to run SQL files
def run(file):
    db = connect()
    for statement in open(file).read().split(';'):
        if statement.strip():
            execute(db, statement)
    disconnect(db)