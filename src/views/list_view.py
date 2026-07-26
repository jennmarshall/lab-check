import customtkinter as ctk
 
 
def fetch_items_from_database():
    """Simulates a database call. Swap this out for a real query later."""
    return [
        {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 24.99, "stock": 58},
        {"id": 2, "name": "Mechanical Keyboard", "category": "Electronics", "price": 89.50, "stock": 12},
        {"id": 3, "name": "Notebook", "category": "Stationery", "price": 3.25, "stock": 210},
        {"id": 4, "name": "Desk Lamp", "category": "Home", "price": 34.00, "stock": 0},
        {"id": 5, "name": "Water Bottle", "category": "Lifestyle", "price": 15.75, "stock": 76},
        {"id": 6, "name": "Monitor Stand", "category": "Electronics", "price": 42.00, "stock": 23},
    ]
 
 
class AbstractListView(ctk.CTkFrame):
    # def __init__(self, connection, master, fetch_func=fetch_items_from_database, **kwargs):
    #     super().__init__(master, **kwargs)
 
    #     self.connection = connection
    #     self.fetch_func = fetch_func
    #     self.items = []
 
    #     # Let the content area expand to fill the page
    #     self.grid_rowconfigure(1, weight=1)
    #     self.grid_columnconfigure(0, weight=1)
 
    #     self._build_header()
    #     self._build_list_area()
 
    #     self.refresh()
 
    # # -- UI construction ---------------------------------------------------
 
    # def _build_header(self):
    #     header = ctk.CTkFrame(self, fg_color="transparent")
    #     header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
    #     header.grid_columnconfigure(0, weight=1)
 
    #     title = ctk.CTkLabel(
    #         header,
    #         text="Inventory Items",
    #         font=ctk.CTkFont(size=20, weight="bold"),
    #     )
    #     title.grid(row=0, column=0, sticky="w")
 
    #     refresh_btn = ctk.CTkButton(
    #         header,
    #         text="Refresh",
    #         width=100,
    #         command=self.refresh,
    #     )
    #     refresh_btn.grid(row=0, column=1, sticky="e")
 
    # def _build_list_area(self):
    #     # Scrollable container — this is the CTk equivalent of a scrollable
    #     # Frame; it behaves like a normal CTkFrame for placing child widgets.
    #     self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="")
    #     self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    #     self.scroll_frame.grid_columnconfigure(0, weight=1)
 
    # # -- Data handling -------------------------------------------------------
 
    # def refresh(self):
    #     """Re-fetches data and redraws the list."""
    #     self.items = self.fetch_func()
    #     self._render_items()
 
    # def _render_items(self):
    #     # Clear any existing rows before redrawing
    #     for widget in self.scroll_frame.winfo_children():
    #         widget.destroy()
 
    #     if not self.items:
    #         empty_label = ctk.CTkLabel(self.scroll_frame, text="No items found.")
    #         empty_label.grid(row=0, column=0, pady=20)
    #         return
 
    #     for row_index, item in enumerate(self.items):
    #         self._render_item_row(row_index, item)
 
    # def _render_item_row(self, row_index, item):
    #     row = ctk.CTkFrame(self.scroll_frame, corner_radius=8)
    #     row.grid(row=row_index, column=0, sticky="ew", pady=6, padx=4)
    #     row.grid_columnconfigure(1, weight=1)
 
    #     # Name + category
    #     name_label = ctk.CTkLabel(
    #         row,
    #         text=item["name"],
    #         font=ctk.CTkFont(size=14, weight="bold"),
    #         anchor="w",
    #     )
    #     name_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 0))
 
    #     category_label = ctk.CTkLabel(
    #         row,
    #         text=item["category"],
    #         text_color=("gray40", "gray70"),
    #         anchor="w",
    #     )
    #     category_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 10))
 
    #     # Price
    #     price_label = ctk.CTkLabel(row, text=f"${item['price']:.2f}", width=80)
    #     price_label.grid(row=0, column=2, rowspan=2, padx=15)
 
    #     # Stock — colored based on availability
    #     in_stock = item["stock"] > 0
    #     stock_text = f"{item['stock']} in stock" if in_stock else "Out of stock"
    #     stock_color = ("green", "#4CAF50") if in_stock else ("red", "#E57373")
 
    #     stock_label = ctk.CTkLabel(row, text=stock_text, text_color=stock_color, width=100)
    #     stock_label.grid(row=0, column=3, rowspan=2, padx=(0, 15))
    
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

class ListAllView(AbstractListView):
    pass

class ListBorrowedView(AbstractListView):
    pass

class ListFilteredView(AbstractListView):
    pass