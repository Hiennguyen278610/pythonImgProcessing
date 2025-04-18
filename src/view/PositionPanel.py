from src.view.component.EntityFrame import EntityFrame
from src.view.Dialog.PositionDialog import AddPositionDialog, EditPositionDialog, ViewPositionDialog
from tkinter import messagebox


class PositionPanel(EntityFrame):

    def __init__(self, master, controller, **kwargs):
        columns = [
            {"field": "ma_chuc_vu", "header": "Mã chức vụ", "width": 1},
            {"field": "ten_chuc_vu", "header": "Tên chức vụ", "width": 3},
            {"field": "ma_phong", "header": "Mã phòng", "width": 2},
        ]

        super().__init__(
            master=master,
            title="Quản Lý Chức Vụ",
            columns=columns,
            controller=controller,
            **kwargs
        )

        # Selected position
        self.selected_position = None

    def onSearch(self, search_text):
        if search_text:
            results = self.controller.search(search_text)
            self.table.updateDataTable(results)
        else:
            self.loadData()

    def onAdd(self):
        AddPositionDialog(self, self.saveNewPosition)

    def onEdit(self):
        if not self.table.getSelected():
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một chức vụ để sửa")
            return

        EditPositionDialog(self, self.table.getSelected(), self.saveEditedPosition)

    def onDelete(self):
        selected = self.table.getSelected()
        if not selected:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một chức vụ để xóa")
            return

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Xác Nhận Xóa",
            f"Bạn có chắc chắn muốn xóa chức vụ: {selected.ten_chuc_vu}?"
        )

        if confirm:
            success, message = self.controller.delete(selected.ma_chuc_vu)
            if success:
                messagebox.showinfo("Thành Công", message)
                self.loadData()  # Refresh table
            else:
                messagebox.showerror("Lỗi", message)

    def onView(self):
        if not self.table.getSelected():
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một chức vụ để xem")
            return

        ViewPositionDialog(self, self.table.getSelected())

    def onRowSelect(self, selected_item):
        self.selected_position = selected_item
        self.crudTool.enableItemButtons(True)

    def saveNewPosition(self, ma_phong, ten_chuc_vu):
        success, message = self.controller.add(ma_phong, ten_chuc_vu)

        if success:
            messagebox.showinfo("Thành Công", message)
            self.loadData()
        else:
            messagebox.showerror("Lỗi", message)

    def saveEditedPosition(self, ma_chuc_vu, ma_phong, ten_chuc_vu):
        success, message = self.controller.update(ma_chuc_vu, ma_phong, ten_chuc_vu)

        if success:
            messagebox.showinfo("Thành Công", message)
            self.loadData()
        else:
            messagebox.showerror("Lỗi", message)