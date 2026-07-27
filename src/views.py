import customtkinter as ctk

import database as db
from models.borrower import Borrower
from models.equipment import Equipment

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
        for view in (MainView, ListAllView, ListBorrowedView, ListFilteredView, AbstractAddView, AbstractEditView):
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

    def fetch_equipment_from_database(self):
        items = []

        rows = db.read(
            db=self.connection,
            select="id, name, category, dateBorrowed, laboratory, status, borrower",
            table="equipment",
            where="1=1",
        )

        for row in rows:
            item_id, name, category, date_borrowed, laboratory, status, borrower = row

            item = {
                "id": item_id,
                "name": name,
                "category": category,
                "dateBorrowed": date_borrowed,
                "laboratory": laboratory,
                "status": status,
                "borrower": borrower,
            }

            items.append(item)

        return items


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
            command=lambda: self.controller.show_frame(AbstractAddView),
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
        self.items = self.controller.fetch_equipment_from_database()
        self._render_items()

    def _render_items(self):
        # Clear any existing rows before redrawing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if self.items == []:
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
            command=lambda item=item: self.controller.show_frame(AbstractEditView, item=item),
        )
        edit_btn.grid(row=0, column=4, rowspan=2, padx=(0, 20))

class ListAllView(AbstractListView):
    pass

class ListBorrowedView(AbstractListView):
# add filter using db query, select = *, from = equipment, where = status is "Borrowed"
    pass

class ListFilteredView(AbstractListView):
# add filter using db query, select = *, from = equipment, where = user input
    pass

class AbstractAddEditView(ctk.CTkFrame):
    STATUS_OPTIONS = ["Borrowed", "Returned", "Overdue"]
    
    def __init__(self, connection, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.connection = connection
        self.controller = controller
        self.item = controller.selected_item
        self.mode = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_form_area()
        self._populate_fields()

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

        title_text = "Edit Borrowed Item" if self.mode == "edit" else "Add Borrowed Item" if self.mode == "add" else "Borrowed Item"
        title = ctk.CTkLabel(
            header,
            text=title_text,
            font=ctk.CTkFont(size=25, weight="bold"),
        )
        title.grid(row=0, column=1, sticky="w")

    def _build_form_area(self):
        self.form_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 15))
        self.form_frame.grid_columnconfigure(0, weight=1)

        self.field_widgets = {}
        row = 0

        row = self._render_text_field(row, "name", "Item Name", "e.g. Microscope")
        row = self._render_text_field(row, "category", "Category", "e.g. Optics")
        row = self._render_text_field(row, "laboratory", "Laboratory", "e.g. Lab 3")
        row = self._render_text_field(row, "dateBorrowed", "Date Borrowed", "YYYY-MM-DD")
        row = self._render_status_field(row)
        row = self._render_borrower_field(row)

        self._build_footer()

    def _render_text_field(self, row_index, name, label_text, placeholder):
        label = ctk.CTkLabel(
            self.form_frame,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=(15, 4))

        entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text=placeholder,
            height=40,
            corner_radius=5,
        )
        entry.grid(row=row_index + 1, column=0, sticky="ew", padx=10, pady=(0, 5))

        self.field_widgets[name] = entry
        return row_index + 2

    def _render_status_field(self, row_index):
        label = ctk.CTkLabel(
            self.form_frame,
            text="Status",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=(15, 4))

        self.status_var = ctk.StringVar(value=self.STATUS_OPTIONS[0])

        status_dropdown = ctk.CTkOptionMenu(
            self.form_frame,
            values=self.STATUS_OPTIONS,
            variable=self.status_var,
            height=40,
            corner_radius=5,
        )
        status_dropdown.grid(row=row_index + 1, column=0, sticky="ew", padx=10, pady=(0, 5))
        return row_index + 2

    def _render_borrower_field(self, row_index):
        label = ctk.CTkLabel(
            self.form_frame,
            text="Borrower",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        label.grid(row=row_index, column=0, sticky="w", padx=10, pady=(15, 4))

        borrower_row = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        borrower_row.grid(row=row_index + 1, column=0, sticky="ew", padx=10, pady=(0, 5))
        borrower_row.grid_columnconfigure(0, weight=1)

        self.borrower_var = ctk.StringVar()
        self.borrower_combo = ctk.CTkComboBox(
            borrower_row,
            values=self.get_borrowers(),
            variable=self.borrower_var,
            height=40,
            corner_radius=5,
        )
        self.borrower_combo.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        add_borrower_btn = ctk.CTkButton(
            borrower_row,
            text="Add",
            width=40,
            height=40,
            corner_radius=5,
            font=ctk.CTkFont(size=14),
            command=self._open_new_borrower_popup,
        )
        add_borrower_btn.grid(row=0, column=1)

        return row_index + 2

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 30))
        footer.grid_columnconfigure(0, weight=1)

        save_btn = ctk.CTkButton(
            footer,
            text="Save",
            width=120,
            height=44,
            corner_radius=5,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_save_clicked,
        )
        save_btn.grid(row=0, column=1, padx=(10, 0))

        cancel_btn = ctk.CTkButton(
            footer,
            text="Cancel",
            width=100,
            height=44,
            corner_radius=5,
            font=ctk.CTkFont(size=14),
            command=self.on_cancel,
        )
        cancel_btn.grid(row=0, column=2, padx=(10, 0))

    # -- New borrower popup ---------------------------------------------------

    def _open_new_borrower_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("New Borrower")
        popup.geometry("600x3180")
        popup.grab_set()

        popup.grid_columnconfigure(3, weight=1)

        label = ctk.CTkLabel(
            popup,
            text="Borrower Name",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 4))

        name_entry = ctk.CTkEntry(
            popup,
            placeholder_text="e.g. J. Smith",
            height=40,
            corner_radius=5,
        )
        name_entry.grid(row=1, column=0, sticky="ew", padx=20)

        number_entry = ctk.CTkEntry(
            popup,
            placeholder_text="e.g. 123-456-7890",
            height=40,
            corner_radius=5,
        )
        number_entry.grid(row=1, column=1, sticky="ew", padx=20)

        email_entry = ctk.CTkEntry(
            popup,
            placeholder_text="e.g. jonsmith123@gmail.com",
            height=40,
            corner_radius=5,
        )
        email_entry.grid(row=1, column=2, sticky="ew")

        error_label = ctk.CTkLabel(popup, text="", text_color=("red", "#E57373"))
        error_label.grid(row=2, column=0, padx=20, pady=(4, 0))

        button_row = ctk.CTkFrame(popup, fg_color="transparent")
        button_row.grid(row=3, columnspan=3, pady=20)

        def on_confirm():
            new_name = name_entry.get().strip()
            new_number = number_entry.get().strip()
            new_email = email_entry.get().strip()
            if not new_name or not new_number or not new_email:
                error_label.configure(text="Fields cannot be empty.")
                return

            borrower = Borrower(new_name, new_number, new_email)

            id = self.create_borrower(borrower)

            # Refresh combobox values and select the new borrower
            updated_borrowers = self.get_borrowers()
            self.borrower_combo.configure(values=updated_borrowers)
            self.borrower_var.set(id)

            popup.destroy()

        confirm_btn = ctk.CTkButton(
            button_row,
            text="Create",
            width=100,
            height=36,
            corner_radius=5,
            command=on_confirm,
        )
        confirm_btn.grid(row=0, column=0, padx=(0, 10))

        cancel_btn = ctk.CTkButton(
            button_row,
            text="Cancel",
            width=100,
            height=36,
            corner_radius=5,
            border_width=1,
            command=popup.destroy,
        )
        cancel_btn.grid(row=0, column=1)

    # -- Data handling -------------------------------------------------------

    # self populates fields if editing
    def _populate_fields(self):
        if self.mode != "edit" or not self.item:
            return

        for name, widget in self.field_widgets.items():
            widget.insert(0, str(self.item.get(name, "")))

        self.status_var.set(self.item.get("status", self.STATUS_OPTIONS[0]))
        self.borrower_var.set(self.item.get("borrower", ""))

    def _collect_field_values(self):
        values = {name: widget.get() for name, widget in self.field_widgets.items()}
        values["status"] = self.status_var.get()
        values["borrower"] = self.borrower_var.get()
        return values

    def _on_save_clicked(self):
        values = self._collect_field_values()        
        equipment = Equipment(values["name"], values["category"], values["dateBorrowed"], values["laboratory"], values["status"], values["borrower"])

        self.on_save_success(equipment)


    def get_borrowers(self):
        borrowers = []
        values = db.read(self.connection, "*", "borrower", "1=1")
        for row in values:
                    borrower_id, name, number, email = row
        
                    borrower = {
                        "id": borrower_id,
                        "name": name,
                        "number": number,
                        "email": email,
                    }
        
                    borrowers.append(borrower)
        
        return borrower

    def create_borrower(self, borrower):
        id = db.create_borrower(self.connection, borrower)
        return id

    def create_equipment(self, equipment):
        id = db.create_equipment(self.connection, equipment)
        return id

    def update_equipment(self, id, equipment):
        db.update_equipment(self.connection, id, equipment)

    def on_save_success(self, equipment):
        if self.mode == "add":
            id = self.create_equipment(equipment)
        elif self.mode == "edit":
            id = self.update_equipment(equipment)
        print(f"INFO: Equipment save successful")
        self.controller.show_frame(ListAllView)

    def on_cancel(self):
        self.controller.show_frame(ListAllView)


class AbstractAddView(AbstractAddEditView):
    def __init__(self, connection, parent, controller):
        super().__init__(connection, parent, controller)
        self.mode = "add"

class AbstractEditView(AbstractAddEditView):
    def __init__(self, connection, parent, controller):
            super().__init__(connection, parent, controller)
            self.mode = "add"