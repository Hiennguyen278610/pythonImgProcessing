from customtkinter import CTkLabel
from src.controller.DepartmentController import DepartmentController
from src.view.component.EntityFrame import EntityFrame
from src.view.dialog.departmentDialog import DepartmentDialog

class DepartmentPanel(EntityFrame):
    def __init__(self, master, **kwargs):
        columns = [
            {"header": "Mã Phòng", "field": "ma_phong", "width": 50},
            {"header": "Mã Trưởng Phòng", "field": "ma_truong_phong", "width": 100},
            {"header": "Tên Phòng", "field": "ten_phong", "width": 200}
        ]

        super().__init__(master,title = "Quản lí phòng ban",columns = columns,controller = DepartmentController(),**kwargs)
        self.selected_department = None
        self.loadData()


    def onSearch(self, search_text):
        data = self.controller.search(search_text)
        self.table.updateDataTable(data)


    def onAdd(self):
        DepartmentDialog(self,self.controller)

    def onEdit(self):
        if self.selected_department:
            department = self.controller.getById(self.selected_department[0])
            if department:
                DepartmentDialog(self,self.controller,department)


    def onDelete(self):
        if self.selected_department:
            if self.controller.delete(self.selected_department[0]):
                self.loadData()
                self.selected_department = None


    def onView(self):
        if self.selected_department:
            department = self.controller.getById(self.selected_department[0])
            if department:
                DepartmentDialog(self,self.controller,department,view_only=True)


    def onRowSelect(self, selected_item):
        self.selected_department = selected_item


