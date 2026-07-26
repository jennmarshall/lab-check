import customtkinter as ctk

class AbstractAddEditView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
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
