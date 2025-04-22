from customtkinter import CTkFrame, CTkButton
from src.view.colorVariable import *

configButton = {
    "fg_color": bgClr,
    "text_color": textClr,
    "border_color": borderClr,
    "border_width": 2,
}

class CRUDToolbar(CTkFrame):
    def __init__(self, master, addCallback=None, editCallback=None, deleteCallback=None, viewCallback=None, **kwargs):
        super().__init__(master, fg_color="white",**kwargs)

        self.addCallback = addCallback
        self.editCallback = editCallback
        self.deleteCallback = deleteCallback
        self.viewCallback = viewCallback

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.addBtn = CTkButton(self, text="Thêm", command=self.onAdd, **configButton)
        self.addBtn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.editBtn = CTkButton(self, text="Sửa", command=self.onEdit, **configButton)
        self.editBtn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.deleteBtn = CTkButton(self, text="Xóa", command=self.onDelete, **configButton)
        self.deleteBtn.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.viewBtn = CTkButton(self, text="Chi tiết", command=self.onView, **configButton)
        self.viewBtn.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        self.enableItemButtons(False)

    def onAdd(self):
        if self.addCallback:
            self.addCallback()

    def onEdit(self):
        if self.editCallback:
            self.editCallback()

    def onDelete(self):
        if self.deleteCallback:
            self.deleteCallback()

    def onView(self):
        if self.viewCallback:
            self.viewCallback()

    def enableItemButtons(self, enable=True):
        state = "normal" if enable else "disabled"
        self.editBtn.configure(state=state)
        self.deleteBtn.configure(state=state)
        self.viewBtn.configure(state=state)