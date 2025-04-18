from customtkinter import CTkFrame
from src.view.component.toolbar.FilterToolbar import FilterToolbar
from src.view.component.toolbar.CRUDToolbar import CRUDToolbar
from src.view.component.table.DataTable import DataTable

class EntityFrame(CTkFrame):
    """Abstract frame combining a filter toolbar, CRUD toolbar, and a data table."""

    def __init__(self, master, title, columns, controller, searchFields=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.title = title
        self.searchFields = searchFields or []

        # Configure overall layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)

        # Header containing filter and CRUD toolbars
        self.header = CTkFrame(self)
        self.header.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,5))
        self.header.grid_rowconfigure(0, weight=1)
        self.header.grid_rowconfigure(1, weight=1)
        self.header.grid_columnconfigure(0, weight=1)

        # Filter toolbar (searchFields must be provided by subclass)
        self.filterTool = FilterToolbar(
            self.header,
            searchFields=self.searchFields,
            searchCallback=self.onSearch,
            resetCallback=self.onReset
        )
        self.filterTool.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # CRUD toolbar
        self.crudTool = CRUDToolbar(
            self.header,
            addCallback=self.onAdd,
            editCallback=self.onEdit,
            deleteCallback=self.onDelete,
            viewCallback=self.onView
        )
        self.crudTool.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Content area with DataTable
        self.content = CTkFrame(self)
        self.content.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5,10))
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Initialize DataTable
        self.table = DataTable(
            self.content,
            columns=columns,
            rowSelectCallback=self.onRowSelect
        )
        self.table.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

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
