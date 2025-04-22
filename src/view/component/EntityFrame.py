from customtkinter import CTkFrame
from src.view.component.toolbar.FilterToolbar import FilterToolbar
from src.view.component.toolbar.CRUDToolbar import CRUDToolbar
from src.view.component.table.DataTable import DataTable
from src.view.colorVariable import *
from src.utils.viewExtention import configFrame

class EntityFrame(CTkFrame):

    def __init__(self, master, title, columns, controller, searchFields=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.title = title
        self.searchFields = searchFields or []
        for i in range(15):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = CTkFrame(self, fg_color=bgClr, **configFrame())
        self.header.grid(row=0, column=0, sticky="nsew", rowspan=2, padx=10)
        self.header.grid_propagate(False)
        for i in range(2):
            self.header.grid_rowconfigure(i, weight=1)
        self.header.grid_columnconfigure(0, weight=1)

        # Filter toolbar (searchFields must be provided by subclass)
        self.filterTool = FilterToolbar(
            self.header,
            searchFields=self.searchFields,
            searchCallback=self.onSearch,
            resetCallback=self.onReset
        )
        self.filterTool.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # CRUD toolbar
        self.crudTool = CRUDToolbar(
            self.header,
            addCallback=self.onAdd,
            editCallback=self.onEdit,
            deleteCallback=self.onDelete,
            viewCallback=self.onView
        )
        self.crudTool.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        # Content area with DataTable
        self.content = CTkFrame(self, fg_color="white", **configFrame(10))
        self.content.grid(row=2, column=0, sticky="nsew", rowspan=13, padx=10, pady=10)
        self.content.grid_propagate(False)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Initialize DataTable
        self.table = DataTable(
            self.content,
            columns=columns,
            rowSelectCallback=self.onRowSelect,
            fg_color="transparent",
            **configFrame()
        )
        self.table.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # Load initial data
        self.loadData()

    def loadData(self):
        data = self.controller.getAll()
        self.table.updateDataTable(data)

    def onSearch(self, *args, **kwargs):
        raise NotImplementedError

    def onReset(self):
        self.loadData()

    def onAdd(self):
        raise NotImplementedError

    def onEdit(self):
        raise NotImplementedError

    def onDelete(self):
        raise NotImplementedError

    def onView(self):
        raise NotImplementedError

    def onRowSelect(self, selected_item):
        raise NotImplementedError
