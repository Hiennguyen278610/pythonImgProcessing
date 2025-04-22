from src.view.BasePanel import BasePanel
from src.controller.ContractController import ContractController

class ContractPanel(BasePanel):
    def __init__(self, master, **kwargs):
        columns = [
            {"field": "ma_hop_dong", "header": "ID", "width": 1},
            {"field": "ma_nhan_vien", "header": "Mã NV", "width": 1},
            {"field": "thoi_han", "header": "Thời hạn", "width": 2},
            {"field": "ngay_ky", "header": "Ngày ký", "width": 2},
            {"field": "muc_luong", "header": "Lương", "width": 3}
        ]
        search_fields = [
            {"label": "Mã hợp đồng", "field": "ma_hop_dong"},
            {"label": "Mã nhân viên", "field": "ma_nhan_vien"},
            {"label": "Thời hạn", "field": "thoi_han"},
            {"label": "Ngày ký", "field": "ngay_ky"},
            {"label": "Lương", "field": "muc_luong"},
        ]
        controller = ContractController()
        super().__init__(master, title="Hợp đồng", columns=columns, controller=controller, searchFields=search_fields, **kwargs)
    
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