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
#     create_borrower_statement = f'''INSERT INTO borowers (name, email, phone)
#         VALUES ('{borrower.name}', '{borrower.email}', '{borrower.phone}');'''
#     execute(db, create_borrower_statement)

# def create_item(db, item):
#     create_item_statement = f'''INSERT INTO items (name, category, date, location, status, contact)
#         VALUES ('{item.name}', '{item.category}', '{item.date}', '{item.location}', '{item.status}', '{item.contact}');'''
#     execute(db, create_item_statement)

# def read_borrower(db, borrower):
#     read_borrower_statement = f'''SELECT * FROM borowers WHERE id = {borrower.id};'''
#     execute(db, read_borrower_statement)

# def read_item(db, item):
#     read_item_statement = f'''SELECT * FROM items WHERE id = {item.id};'''
#     execute(db, read_item_statement)

# def update_borrower(db, borrower):
#     update_borrower_statement = f'''UPDATE borowers SET name = '{borrower.name}', email = '{borrower.email}', phone = '{borrower.phone}' WHERE id = {borrower.id};'''
#     execute(db, update_borrower_statement)

# def update_item(db, item):
#     update_item_statement = f'''UPDATE items SET name = '{item.name}', category = '{item.category}', date = '{item.date}', location = '{item.location}', status = '{item.status}', contact = '{item.contact}' WHERE id = {item.id};'''
#     execute(db, update_item_statement)

# def delete_borrower(db, borrower):
#     delete_borrower_statement = f'''DELETE FROM borowers WHERE id = {borrower.id};'''
#     execute(db, delete_borrower_statement)

# def delete_item(db, item):
#     delete_item_statement = f'''DELETE FROM items WHERE id = {item.id};'''
#     execute(db, delete_item_statement)

# method to run SQL files
def run(file):
    db = connect()
    for statement in open(file).read().split(';'):
        if statement.strip():
            execute(db, statement)
    disconnect(db)