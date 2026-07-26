import customtkinter as ctk

from views.list_view import ListAllView, ListBorrowedView, ListFilteredView
from views.add_edit_view import AddItemView, AddBorrowerView, EditItemView, EditBorrowerView

class LabCheckView(ctk.CTk):
    def __init__(self, connection, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.connection = connection

        # Creating a container that will be used to define the structure each
        # page of the application.
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Loop through the different pages of the application and create a
        # frame for each page, and subsequently add the frames list.
        for view in (MainView, ListAllView, ListBorrowedView, ListFilteredView, AddItemView, AddBorrowerView, EditItemView, EditBorrowerView):
            frame = view(container, self)
            self.frames[view] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainView)

    # Function to show the frame of the page that is passed as an argument.
    def show_frame(self, f):
        frame = self.frames[f]
        frame.tkraise()



# The definition for the start page of the application, which is the first page
# that is shown when the application is run. It contains a welcome message and
# a button to start the application, which takes the user to the view items
# page.
class MainView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # Make the frames grid center its content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Welcome label
        label_welcome = ctk.CTkLabel(
            self,
            text="Welcome to LabCheck",
            font=("Arial", 20, "bold")
        )

        # Container to hold buttons side by side
        button_frame = ctk.CTkFrame(self, fg_color="transparent")

        button_all_view = ctk.CTkButton(
            button_frame,
            text="View All Items",
            command=lambda: controller.show_frame(ListAllView),
            width=160,
            height=50,
            corner_radius=5,
            font=("Arial", 14, "bold")
        )

        button_borrowed_view = ctk.CTkButton(
            button_frame,
            text="View Borrowed Items",
            command=lambda: controller.show_frame(ListBorrowedView),
            width=160,
            height=50,
            corner_radius=5,
            font=("Arial", 14, "bold")
        )

        # Evenly space buttons within their container
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        button_all_view.grid(row=0, column=0, padx=20, pady=10)
        button_borrowed_view.grid(row=0, column=1, padx=20, pady=10)

        # Place label and button_frame centered in the window
        label_welcome.grid(row=0, column=0, pady=(0, 10), sticky="s")
        button_frame.grid(row=1, column=0, sticky="n")