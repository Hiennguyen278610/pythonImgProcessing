from pyexpat.errors import messages
from tkinter import messagebox

from customtkinter import CTkLabel
from src.controller.DepartmentController import DepartmentController
from src.view.component.EntityFrame import EntityFrame
from src.view.component.toolbar.FilterToolbar import FilterToolbar
from src.view.dialog.DepartmentDialog import DepartmentDialog

class DepartmentPanel(EntityFrame):
    def __init__(self, master,**kwargs):
        columns = [
            {"field": "ma_phong","header": "Mã Phòng","width": 50},
            { "field": "ma_truong_phong","header": "Mã Trưởng Phòng","width": 100},
            {"field": "ten_phong","header": "Tên Phòng" ,"width": 200}
        ]

        search_fields = [
            {"label":"Mã phòng","field":"ma_phong"},
            {"label":"Mã Trưởng Phòng","field":"ma_truong_phong"},
            {"label":"Tên Phòng","field":"ten_phong"},
        ]

        super().__init__(master,title = "Quản lí phòng ban",columns = columns,controller = DepartmentController(),searchFields=search_fields,**kwargs)
        self.filterTool.destroy()
        self.filterTool = FilterToolbar(self.header,searchFields=search_fields,searchCallback=self.onSearch,resetCallback=self.onReset)
        self.filterTool.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.selected_department = None
        self.loadData()


    def onSearch(self, search_text,keyword):
        if keyword:
            data = self.controller.search(search_text,keyword)
            self.table.updateDataTable(data)
        else:
            self.loadData()

    def onReset(self):
        self.table.updateDataTable([])
        self.loadData()

    def onAdd(self):
        DepartmentDialog(self,self.controller)

    def onEdit(self):
        if not self.selected_department:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một phòng ban để sửa")
            return

        department = self.controller.getById(self.selected_department.ma_phong)
        if department:
            DepartmentDialog(self, self.controller, department)

    def onDelete(self):
        if self.selected_department:
            if self.controller.delete(self.selected_department.ma_phong):
                self.loadData()
                self.selected_department = None
                self.crudTool.enableItemButtons(False)

    def onView(self):
        if not self.selected_department:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một phòng ban để xem")
            return

        department = self.controller.getById(self.selected_department.ma_phong)
        if department:
            DepartmentDialog(self, self.controller, department, view_only=True)

    def onRowSelect(self, selected_item):
        self.selected_department = selected_item
        self.crudTool.enableItemButtons(True)


