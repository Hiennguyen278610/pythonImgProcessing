from customtkinter import CTkFrame
from src.view.component.EntityFrame import EntityFrame
from CTkMessagebox import *
from src.utils.messageUtil import show_info, show_warning, show_error
from src.view.colorVariable import * 

class BasePanel(CTkFrame):
    def __init__(self, master, title, columns, controller, **kwargs):
        searchFields = kwargs.pop("searchFields", [])
        super().__init__(master, **kwargs)
        self.title = title
        self.controller = controller
        
        # Cấu hình layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Entity frame
        self.entityFrame = EntityFrame(
            self, 
            title=title,
            columns=columns,
            controller=controller,
            searchFields=searchFields,
            fg_color=bgClr,
            corner_radius=0
        )
        self.entityFrame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Override các phương thức của entityFrame
        self.entityFrame.onSearch = self.onSearch
        self.entityFrame.onAdd = self.onAdd
        self.entityFrame.onEdit = self.onEdit
        self.entityFrame.onDelete = self.onDelete
        self.entityFrame.onView = self.onView
        self.entityFrame.onRowSelect = self.onRowSelect
    
    def onSearch(self, query):
        try:
            if query:
                result = self.controller.searchByName(query)
                self.entityFrame.table.set_data(result)
            else:
                self.entityFrame.loadData()
        except Exception as e:
            self.show_error(f"This message in BasePanel: {str(e)}")
    
    def onAdd(self):
        """Mở dialog thêm mới (được implement bởi lớp con)"""
        pass
    
    def onEdit(self):
        """Mở dialog sửa (được implement bởi lớp con)"""
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Please select a value for update.")
            return
    
    def onDelete(self):
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("PLease select a value for delete.")
            return
        confirm = CTkMessagebox(
            title="Confirm delete ????",
            message=f"Are you sure delete {self.title.lower()} ???",
            icon="question",
            option_1="Yes",
            option_2="No"
        )
        if confirm.get() == "Yes":
            try:
                id_field = self.getIDField()
                if hasattr(selected, id_field):
                    self.controller.delete(getattr(selected, id_field))
                    self.entityFrame.loadData()
                    self.show_info(f"Delete {self.title.lower()} is done.")
            except Exception as e:
                self.show_error(f"This message in BasePanel: {str(e)}")
    
    def onView(self):
        """Mở dialog xem chi tiết (được implement bởi lớp con)"""
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Vui lòng chọn một dòng để xem chi tiết")
            return
    
    def onRowSelect(self, selectedItem):
        """Xử lý khi chọn một dòng trong bảng"""
        if selectedItem:
            self.entityFrame.crudTool.enable_item_buttons(True)
        else:
            self.entityFrame.crudTool.enable_item_buttons(False)
    
    def getIDField(self):
        """Trả về tên trường ID của đối tượng (override bởi lớp con)"""
        return "id"
    
    def refresh(self):
        """Làm mới dữ liệu"""
        self.entityFrame.loadData()

    def show_info(self, message):
        show_info(message)

    def show_warning(self, message):
        show_warning(message)

    def show_error(self, message):
        show_error(message)