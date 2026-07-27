import customtkinter as ctk


def fetch_items_from_database():
    """Simulates a database call. Swap this out for a real query later."""
    return [
        {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "dateBorrowed": "2026-06-02", "laboratory": "Lab 1", "status": "Borrowed", "borrower": "J. Smith"},
        {"id": 2, "name": "Mechanical Keyboard", "category": "Electronics", "dateBorrowed": "2026-05-14", "laboratory": "Lab 2", "status": "Overdue", "borrower": "A. Patel"},
        {"id": 3, "name": "Notebook", "category": "Stationery", "dateBorrowed": "2026-07-01", "laboratory": "Lab 1", "status": "Returned", "borrower": "M. Chen"},
        {"id": 4, "name": "Desk Lamp", "category": "Home", "dateBorrowed": "2026-06-20", "laboratory": "Lab 3", "status": "Borrowed", "borrower": "R. Okafor"},
        {"id": 5, "name": "Water Bottle", "category": "Lifestyle", "dateBorrowed": "2026-04-30", "laboratory": "Lab 2", "status": "Returned", "borrower": "S. Kim"},
        {"id": 6, "name": "Monitor Stand", "category": "Electronics", "dateBorrowed": "2026-07-15", "laboratory": "Lab 3", "status": "Overdue", "borrower": "L. Novak"},
    ]

class LabCheckView(ctk.CTk):
    def __init__(self, connection, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.connection = connection
        self.frames = {}
        self.selected_item = None

        # Creating a container that will be used to define the structure each
        # page of the application.
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Loop through the different pages of the application and create a
        # frame for each page, and subsequently add the frames list.
        for view in (MainView, ListAllView, ListBorrowedView, ListFilteredView, AddItemView, AddBorrowerView, EditItemView, EditBorrowerView):
            frame = view(connection, container, self)
            self.frames[view] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainView)

    # Function to show the frame of the page that is passed as an argument.
    def show_frame(self, f, *args):
        if args:
            self.selected_item = args[0]
        frame = self.frames[f]
        frame.tkraise()



# The definition for the start page of the application, which is the first page
# that is shown when the application is run. It contains a welcome message and
# a button to start the application, which takes the user to the view items
# page.
class MainView(ctk.CTkFrame):
    def __init__(self, connection, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.connection = connection

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
            text="View All Equipment",
            command=lambda: controller.show_frame(ListAllView),
            width=160,
            height=50,
            corner_radius=5,
            font=("Arial", 14, "bold")
        )

        button_borrowed_view = ctk.CTkButton(
            button_frame,
            text="View Borrowed Equipment",
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


class AbstractListView(ctk.CTkFrame):
    def __init__(self, connection, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.connection = connection
        self.controller = controller
        self.items = []

        # Let the content area expand to fill the page
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_list_area()

        self.refresh()

    # -- UI construction ---------------------------------------------------

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 15))
        header.grid_columnconfigure(1, weight=1)

        home_btn = ctk.CTkButton(
            header,
            text="Home",
            width=40,
            height=40,
            corner_radius=5,
            font=ctk.CTkFont(size=16),
            border_width=1,
            command=lambda: self.controller.show_frame(MainView),
        )
        home_btn.grid(row=0, column=0, padx=(0, 15))

        title = ctk.CTkLabel(
            header,
            text="Laboratory Equipment",
            font=ctk.CTkFont(size=25, weight="bold"),
        )
        title.grid(row=0, column=1, sticky="w")

        # Search / edit button (inline with refresh)
        search_btn = ctk.CTkButton(
            header,
            text="Search",
            width=40,
            height=40,
            corner_radius=5,
            font=ctk.CTkFont(size=16),
            command=lambda: self.controller.show_frame(ListFilteredView),
        )
        search_btn.grid(row=0, column=2, padx=(0, 10))

        # Refresh button — square
        refresh_btn = ctk.CTkButton(
            header,
            text="Refresh",
            width=40,
            height=40,
            corner_radius=5,
            font=ctk.CTkFont(size=16),
            command=self.refresh,
        )
        refresh_btn.grid(row=0, column=3, padx=(0, 10))

        # Add button — top right corner
        add_btn = ctk.CTkButton(
            header,
            text="Add",
            width=40,
            height=40,
            corner_radius=5,
            font=ctk.CTkFont(size=16),
            command=lambda: self.controller.show_frame(AddItemView),
        )
        add_btn.grid(row=0, column=4, padx=(0, 10))

    def _build_list_area(self):
        # Scrollable container — this is the CTk equivalent of a scrollable
        # Frame; it behaves like a normal CTkFrame for placing child widgets.
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 30))
        self.scroll_frame.grid_columnconfigure(0, weight=1)

    # -- Data handling -------------------------------------------------------

    def refresh(self):
        self.items = fetch_items_from_database()
        self._render_items()

    def _render_items(self):
        # Clear any existing rows before redrawing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not self.items:
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="No items found.",
                font=ctk.CTkFont(size=14),
                text_color=("gray40", "gray70"),
            )
            empty_label.grid(row=0, column=0, pady=40)
            return

        for row_index, item in enumerate(self.items):
            self._render_item_row(row_index, item)

    def _render_item_row(self, row_index, item):
        row = ctk.CTkFrame(self.scroll_frame, corner_radius=8)
        row.grid(row=row_index, column=0, sticky="ew", pady=8, padx=6)
        row.grid_columnconfigure(1, weight=1)

        # Name + category
        name_label = ctk.CTkLabel(
            row,
            text=item["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        name_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(16, 0))

        category_label = ctk.CTkLabel(
            row,
            text=item["category"],
            text_color=("gray40", "gray70"),
            anchor="w",
        )
        category_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 16))

        laboratory_label = ctk.CTkLabel(
            row,
            text=item["laboratory"],
            text_color=("gray40", "gray70"),
            anchor="w",
        )
        laboratory_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 16))

        status = item["status"]
        if status == "Returned":
            stock_color = ("green", "#4CAF50")
        elif status == "Overdue":
            stock_color = ("red", "#E57373")
        else:
            stock_color = ("gray40", "gray70")
        status_label = ctk.CTkLabel(
            row,
            text=item["status"],
            text_color=stock_color,
            anchor="w",
        )
        status_label.grid(row=0, column=2, rowspan=2, padx=20, pady=(16, 0))

        date_borrowed_label = ctk.CTkLabel(
            row,
            text=item["dateBorrowed"],
            text_color=("gray40", "gray70"),
            anchor="w",
        )
        date_borrowed_label.grid(row=2, column=2, padx=20, pady=(0, 16))

        borrower_label = ctk.CTkLabel(
            row,
            text=item["borrower"],
            text_color=("gray40", "gray70"),
            anchor="w",
        )
        borrower_label.grid(row=2, column=3, padx=20, pady=(0, 16))

        # Edit button — per item
        edit_btn = ctk.CTkButton(
            row,
            text="Edit",
            width=40,
            height=40,
            corner_radius=5,
            font=ctk.CTkFont(size=16),
            command=lambda item=item: self.controller.show_frame(EditItemView, item=item),
        )
        edit_btn.grid(row=0, column=4, rowspan=2, padx=(0, 20))

class ListAllView(AbstractListView):
    pass

class ListBorrowedView(AbstractListView):
    pass

class ListFilteredView(AbstractListView):
    pass

class AbstractAddEditView(ctk.CTkFrame):
    def __init__(self, connection, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.connection = connection
        self.controller = controller


class AbstractAddView(AbstractAddEditView):
    pass

class AbstractEditView(AbstractAddEditView):
    pass


class AddItemView(AbstractAddView):
    pass

class AddBorrowerView(AbstractAddView):
    pass

class EditItemView(AbstractEditView):
    pass

class EditBorrowerView(AbstractEditView):
    pass
