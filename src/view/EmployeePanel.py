from src.view.BasePanel import BasePanel
from src.controller.EmployeeController import EmployeeController

class EmployeePanel(BasePanel):
    def __init__(self, master, **kwargs):
        # Định nghĩa các cột cho Employee
        columns = [
            {"field": "employeeID", "header": "ID", "width": 1},
            {"field": "name", "header": "Họ tên", "width": 4},
            {"field": "phone", "header": "SĐT", "width": 2},
            {"field": "gender", "header": "Giới tính", "width": 1},
            {"field": "address", "header": "Địa chỉ", "width": 4}
        ]
        
        # Khởi tạo controller
        controller = EmployeeController()
        
        super().__init__(master, title="Nhân viên", columns=columns, controller=controller, **kwargs)
    
    def getIDField(self):
        """Trả về tên trường ID của đối tượng"""
        return "employeeID"
    
    def onAdd(self):
        """Mở dialog thêm mới nhân viên"""
        # TODO: Implement add dialog
        self.show_info("Chức năng thêm nhân viên sẽ được thực hiện sau")
    
    def onEdit(self):
        """Mở dialog sửa nhân viên"""
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Vui lòng chọn một nhân viên để sửa")
            return
        
        # TODO: Implement edit dialog
        self.show_info(f"Sửa nhân viên: {selected.name}")
    
    def onView(self):
        """Mở dialog xem chi tiết nhân viên"""
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Vui lòng chọn một nhân viên để xem chi tiết")
            return
        
        # TODO: Implement view dialog
        self.show_info(f"Xem chi tiết nhân viên: {selected.name}")