from src.view.component.EntityFrame import EntityFrame
from src.view.component.toolbar.FilterToolbar import FilterToolbar
from src.view.Dialog.PositionDialog import AddPositionDialog, EditPositionDialog, ViewPositionDialog
from tkinter import messagebox


class PositionPanel(EntityFrame):
    """Panel quản lý chức vụ với tìm kiếm đa trường chung"""

    def __init__(self, master, controller, **kwargs):
        # Cấu hình cột cho bảng
        columns = [
            {"field": "ma_chuc_vu", "header": "Mã chức vụ", "width": 1},
            {"field": "ten_chuc_vu", "header": "Tên chức vụ", "width": 3},
            {"field": "ma_phong",   "header": "Mã phòng",     "width": 2},
        ]
        # Danh sách các trường cho tìm kiếm chung
        search_fields = [
            {"label": "Mã chức vụ",  "field": "ma_chuc_vu"},
            {"label": "Tên chức vụ", "field": "ten_chuc_vu"},
            {"label": "Mã phòng",    "field": "ma_phong"},
        ]
        # Khởi tạo EntityFrame cơ bản
        super().__init__(
            master=master,
            title="Quản Lý Chức Vụ",
            columns=columns,
            controller=controller,
            searchFields=search_fields,
            **kwargs
        )
        # Thay thế filterTool thành toolbar dùng chung với nhiều trường
        self.filterTool.destroy()
        self.filterTool = FilterToolbar(
            self.header,
            searchFields=search_fields,
            searchCallback=self.onSearch,
            resetCallback=self.onReset
        )
        self.filterTool.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.selected_position = None

    def onSearch(self, field, keyword):
        """Tìm kiếm theo trường field và từ khóa keyword"""
        if keyword:
            results = self.controller.search(field, keyword)
            self.table.updateDataTable(results)
        else:
            self.loadData()

    def onReset(self):
        """Reset bộ lọc, tải lại tất cả dữ liệu"""
        self.table.updateDataTable([])
        self.loadData()

    def onAdd(self):
        AddPositionDialog(self, self.saveNewPosition)

    def onEdit(self):
        if not self.table.getSelected():
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một chức vụ để sửa")
            return
        EditPositionDialog(
            self, self.table.getSelected(), self.saveEditedPosition
        )

    def onDelete(self):
        selected = self.table.getSelected()
        if not selected:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một chức vụ để xóa")
            return
        confirm = messagebox.askyesno(
            "Xác Nhận Xóa",
            f"Bạn có chắc chắn muốn xóa chức vụ: {selected.ten_chuc_vu}?"
        )
        if confirm:
            success, msg = self.controller.delete(selected.ma_chuc_vu)
            if success:
                messagebox.showinfo("Thành Công", msg)
                self.loadData()
            else:
                messagebox.showerror("Lỗi", msg)

    def onView(self):
        if not self.table.getSelected():
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một chức vụ để xem")
            return
        ViewPositionDialog(self, self.table.getSelected())

    def onRowSelect(self, selected_item):
        self.selected_position = selected_item
        self.crudTool.enableItemButtons(True)

    def saveNewPosition(self, ma_chuc_vu, ma_phong, ten_chuc_vu):
        success, msg = self.controller.add(ma_chuc_vu, ma_phong, ten_chuc_vu)
        if success:
            messagebox.showinfo("Thành Công", msg)
            self.loadData()
        else:
            messagebox.showerror("Lỗi", msg)

    def saveEditedPosition(self, ma_chuc_vu, ma_phong, ten_chuc_vu):
        success, msg = self.controller.update(ma_chuc_vu, ma_phong, ten_chuc_vu)
        if success:
            messagebox.showinfo("Thành Công", msg)
            self.loadData()
        else:
            messagebox.showerror("Lỗi", msg)
