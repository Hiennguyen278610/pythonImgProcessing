from tkinter import messagebox
from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkComboBox
from src.model.entity.DepartmentEntity import Department

class DepartmentDialog(CTkToplevel):
    def __init__(self, parent, controller, department=None, view_only=False):
        super().__init__(parent)
        self.controller = controller
        self.department = department
        self.view_only = view_only

        if self.view_only:
            self.title("Xem thông tin phòng ban")
        elif self.department:
            self.title("Chỉnh sửa phòng ban")
        else:
            self.title("Thêm phòng ban")

        self.geometry("500x300")
        self.resizable(False, False)
        self.transient(parent)
        self.focus_set()


        self.update_idletasks()  # Cập nhật layout trước khi lấy kích thước
        window_width = 500
        window_height = 300

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width // 2) - (window_width // 2)
        y = parent_y + (parent_height // 2) - (window_height // 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.init()

    def init(self):
        # Load employee data
        self.employees = self.controller.getAllEmployees()  # List of employee objects
        self.employee_options = []
        self.employee_map = {}

        for emp in self.employees:
            display_text = f"{emp.ma_nhan_vien} - {emp.ho_ten_nhan_vien}"

            self.employee_options.append(display_text)
            self.employee_map[display_text] = emp.ma_nhan_vien

        CTkLabel(self, text="Trưởng phòng: ").pack(pady=5)
        self.ma_truong_phong = CTkComboBox(self, values=self.employee_options)
        self.ma_truong_phong.pack(pady=5)

        CTkLabel(self, text="Tên phòng: ").pack(pady=5)
        self.ten_phong = CTkEntry(self)
        self.ten_phong.pack(pady=5)

        if self.department:
            selected_emp_text = next(
                (text for text, id in self.employee_map.items() if id == self.department.ma_truong_phong), "")
            if selected_emp_text:
                self.ma_truong_phong.set(selected_emp_text)
            self.ten_phong.insert(0, self.department.ten_phong or '')

            if self.view_only:
                self.ma_truong_phong.configure(state="readonly")
                self.ten_phong.configure(state="readonly")

        if not self.view_only:
            CTkButton(self, text="Cập nhật", command=self.save).pack(pady=10)
        CTkButton(self, text="Thoát", command=self.destroy).pack(pady=10)

    def save(self):
        selected = self.ma_truong_phong.get()
        if selected not in self.employee_map:
            messagebox.showerror("Lỗi", "Vui lòng chọn trưởng phòng hợp lệ.")
            return

        ma_truong_phong = self.employee_map[selected]
        ten_phong = self.ten_phong.get().strip()

        if not ten_phong:
            messagebox.showerror("Lỗi", "Tên phòng không được để trống.")
            return

        department_data = {
            'ma_truong_phong': ma_truong_phong,
            'ten_phong': ten_phong
        }

        try:
            if self.department is None:
                self.controller.create(department_data)
                messagebox.showinfo("Thành công", "Thêm phòng ban thành công.")
            else:
                self.controller.update(self.department.ma_phong, department_data)
                messagebox.showinfo("Thành công", "Cập nhật phòng ban thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
            return

        self.master.loadData()
        self.destroy()

    def confirm_delete(self):
        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa phòng ban này không?"):
            try:
                self.controller.delete(self.department.ma_phong)
                messagebox.showinfo("Thành công", "Xóa phòng ban thành công.")
                self.master.loadData()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa: {e}")
