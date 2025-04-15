from src.view.BasePanel import BasePanel
from src.controller.ContractController import ContractController

class ContractPanel(BasePanel):
    def __init__(self, master, **kwargs):
        # Định nghĩa các cột cho Contract
        columns = [
            {"field": "contractID", "header": "ID", "width": 1},
            {"field": "employeeID", "header": "Mã NV", "width": 1},
            {"field": "term", "header": "Thời hạn", "width": 2},
            {"field": "signingDate", "header": "Ngày ký", "width": 2},
            {"field": "salary", "header": "Lương", "width": 3}
        ]
        
        # Khởi tạo controller
        controller = ContractController()
        
        super().__init__(master, title="Hợp đồng", columns=columns, controller=controller, **kwargs)
    
    def getIDField(self):
        """Trả về tên trường ID của đối tượng"""
        return "contractID"
    
    def onAdd(self):
        """Mở dialog thêm mới hợp đồng"""
        # TODO: Implement add dialog
        self.show_info("Chức năng thêm hợp đồng sẽ được thực hiện sau")
    
    def onEdit(self):
        """Mở dialog sửa hợp đồng"""
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Vui lòng chọn một hợp đồng để sửa")
            return
        
        # TODO: Implement edit dialog
        self.show_info(f"Sửa hợp đồng ID: {selected.contractID}")
    
    def onView(self):
        """Mở dialog xem chi tiết hợp đồng"""
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Vui lòng chọn một hợp đồng để xem chi tiết")
            return
        
        # TODO: Implement view dialog
        self.show_info(f"Xem chi tiết hợp đồng ID: {selected.contractID}")