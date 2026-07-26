import tkinter as tk

import database as db
from views.main_view import LabCheckView


# The main file for the LabCheck application, that contains the main function that
# runs the application.

# The main function that runs the application. It creates a connection to the database, initializes the main application window, and starts the main event loop. After the main event loop ends, it will close the database connection. 
def main():
    global connection
    connection = db.connect('database.db')

    root = LabCheckView(connection)
    root.title("LabCheck - Laboratory Equipment Management System")

    # Set the dimensions of the main application window and center it on the
    # screen.
    w_width: int = 1000
    w_height: int = 800

    s_width: int = root.winfo_screenwidth()
    s_height: int = root.winfo_screenheight()

    x = int((s_width/2) - (w_width/2))
    y = int((s_height/2) - (w_height/2))

    root.geometry(f"{w_width}x{w_height}+{x}+{y}")

    root.mainloop()

    db.disconnect(connection)


main()
