from src.view.BasePanel import BasePanel
from src.controller.EmployeeController import EmployeeController


class EmployeePanel(BasePanel):
    def __init__(self, master, **kwargs):
        columns = [
            {"field": "ma_nhan_vien", "header": "Mã NV", "width": 1},
            {"field": "ten_nhan_vien", "header": "Tên NV", "width": 2},
            {"field": "chuc_vu", "header": "Chức vụ", "width": 2},
            {"field": "ngay_sinh", "header": "Ngày sinh", "width": 2},
            {"field": "gioi_tinh", "header": "Giới tính", "width": 1},
        ]
        search_fields = [
            {"label": "Mã nhân viên", "field": "ma_nhan_vien"},
            {"label": "Tên nhân viên", "field": "ten_nhan_vien"},
            {"label": "Chức vụ", "field": "chuc_vu"},
        ]
        controller = EmployeeController()
        super().__init__(master, title="Nhân viên", columns=columns, controller=controller, searchFields=search_fields, **kwargs)

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