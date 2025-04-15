from customtkinter import CTkFrame
from src.view.component.toolbar.FilterToolbar import FilterToolbar
from src.view.component.toolbar.CRUDToolbar import CRUDToolbar
from src.view.component.table.DataTable import DataTable

class EntityFrame(CTkFrame):
    def __init__(self, master, title, columns, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.title = title
        
        # Cấu hình layout
        self.grid_rowconfigure(0, weight=1)  # Header
        self.grid_rowconfigure(1, weight=9)  # Content
        self.grid_columnconfigure(0, weight=1)
        
        # Header chứa filter và CRUD tools
        self.header = CTkFrame(self)
        self.header.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,5))
        self.header.grid_rowconfigure(0, weight=1)  # FilterTool
        self.header.grid_rowconfigure(1, weight=1)  # CRUDTool
        self.header.grid_columnconfigure(0, weight=1)
        
         # Filter toolbar
        self.filterTool = FilterToolbar(
            self.header, 
            searchCallback=self.onSearch,
            resetCallback=self.onReset,
            height=20
        )
        self.filterTool.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # CRUD toolbar
        self.crudTool = CRUDToolbar(
            self.header,
            addCallback=self.onAdd,
            editCallback=self.onEdit,
            deleteCallback=self.onDelete,
            viewCallback=self.onView,
            height=20
        )
        self.crudTool.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Content với DataTable
        self.content = CTkFrame(self)
        self.content.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5,10))
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        
        # DataTable
        self.table = DataTable(
            self.content,
            columns=columns,
            rowSelectCallback=self.onRowSelect
        )
        self.table.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Khởi tạo với dữ liệu
        self.loadData()
        
    def loadData(self):
        """Lấy dữ liệu từ controller và cập nhật bảng"""
        data = self.controller.getAll()
        self.table.updateDataTable(data)
    
    def onSearch(self, search_text):
        """Xử lý khi người dùng tìm kiếm"""
        pass  # Được implement bởi lớp con
    
    def onReset(self):
        """Xử lý khi người dùng reset bộ lọc"""
        self.loadData()
    
    def onAdd(self):
        """Xử lý khi người dùng muốn thêm mới"""
        pass  # Được implement bởi lớp con
    
    def onEdit(self):
        """Xử lý khi người dùng muốn sửa"""
        pass  # Được implement bởi lớp con
    
    def onDelete(self):
        """Xử lý khi người dùng muốn xóa"""
        pass  # Được implement bởi lớp con
    
    def onView(self):
        """Xử lý khi người dùng muốn xem chi tiết"""
        pass  # Được implement bởi lớp con
    
    def onRowSelect(self, selected_item):
        """Xử lý khi người dùng chọn một dòng trong bảng"""
        pass  # Được implement bởi lớp con