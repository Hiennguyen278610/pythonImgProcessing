from src.view.BasePanel import BasePanel
from src.controller.EmployeeController import EmployeeController
from CTkMessagebox import *

class EmployeePanel(BasePanel):
    def __init__(self, master, **kwargs):
        columns = [
            {"field": "ma_nhan_vien", "header": "Mã NV", "width": 1},
            {"field": "ho_ten_nhan_vien", "header": "Tên NV", "width": 2},
            {"field": "ma_chuc_vu", "header": "Chức vụ", "width": 2},
            {"field": "ngay_sinh", "header": "Ngày sinh", "width": 2},
            {"field": "gioi_tinh", "header": "Giới tính", "width": 1},
        ]
        search_fields = [
            {"label": "Mã nhân viên", "field": "ma_nhan_vien"},
            {"label": "Tên nhân viên", "field": "ho_ten_nhan_vien"},
            {"label": "Chức vụ", "field": "ma_chuc_vu"},
        ]
        controller = EmployeeController()
        super().__init__(master, title="Nhân viên", columns=columns, controller=controller, searchFields=search_fields, **kwargs)

    def getIDField(self):
        """Trả về tên trường ID của đối tượng"""
        return "employeeID"

    def onAdd(self):
        """Mở dialog thêm mới nhân viên"""
        from src.view.dialog.EmployeeDialog import EmployeeDialog
        dialog = EmployeeDialog(
            master=self,
            controller=self.controller,
            mode="add",
            callback=self.entityFrame.loadData
        )
        self.wait_window(dialog)

    def onDelete(self):
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Vui lòng chọn một nhân viên để xóa")
            return
        
        ten_nv = getattr(selected, "ho_ten_nhan_vien", "")
        ma_nv = getattr(selected, "ma_nhan_vien", None)
        if ma_nv is None:
            self.show_warning("Không thể xác định mã nhân viên để xóa")
            return
        
        confirm = CTkMessagebox(
            title="Xác nhận xóa",
            message=f"Bạn có chắc chắn muốn xóa nhân viên '{ten_nv}' không?",
            icon="question",
            option_1="Có",
            option_2="Không"
        )
        
        if confirm.get() == "Có":
            try:
                self.controller.delete(ma_nv)
                self.entityFrame.loadData()
                self.show_info(f"Xóa nhân viên '{ten_nv}' thành công")
            except Exception as e:
                self.show_error(f"Lỗi khi xóa nhân viên: {str(e)}")

    def onEdit(self):
        """Mở dialog chỉnh sửa nhân viên"""
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Vui lòng chọn một nhân viên để chỉnh sửa")
            return
            
        from src.view.dialog.EmployeeDialog import EmployeeDialog
        dialog = EmployeeDialog(
            master=self,
            controller=self.controller,
            mode="edit",
            employee=selected,
            callback=self.entityFrame.loadData
        )
        self.wait_window(dialog)

    def onView(self):
        """Mở dialog xem chi tiết nhân viên"""
        selected = self.entityFrame.table.getSelected()
        if not selected:
            self.show_warning("Vui lòng chọn một nhân viên để xem chi tiết")
            return
            
        from src.view.dialog.EmployeeDialog import EmployeeDialog
        dialog = EmployeeDialog(
            master=self,
            controller=self.controller,
            mode="view",
            employee=selected
        )
        self.wait_window(dialog)