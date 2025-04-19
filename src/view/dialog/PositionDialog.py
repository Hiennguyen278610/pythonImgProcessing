from tkinter import messagebox
from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkFrame
from src.model.entity.PositionEntity import Position

class BasePositionDialog(CTkToplevel):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)
        self.transient(parent)
        self.after(10, self.grab_set)
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        width = 400
        height = 250
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_rowconfigure(3, weight=1)

        CTkLabel(main_frame, text="Mã chức vụ:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.id_entry = CTkEntry(main_frame, placeholder_text="Nhập mã chức vụ")
        self.id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        CTkLabel(main_frame, text="Tên chức vụ:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = CTkEntry(main_frame, placeholder_text="Nhập tên chức vụ")
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        CTkLabel(main_frame, text="Mã phòng:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.dept_entry = CTkEntry(main_frame, placeholder_text="Nhập mã phòng")
        self.dept_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        button_frame = CTkFrame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.save_btn = CTkButton(button_frame, text="Lưu", command=self.on_save)
        self.save_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.cancel_btn = CTkButton(button_frame, text="Hủy", command=self.destroy)
        self.cancel_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.name_entry.focus_set()

    def on_save(self):
        pass

    def validate_inputs(self):
        if "readonly" not in self.id_entry.cget("state"):
            position_id = self.id_entry.get().strip()
            if not position_id:
                return False, "Mã chức vụ không được để trống"
            if len(position_id) > 10:
                return False, "Mã chức vụ không được vượt quá 10 ký tự"
        name = self.name_entry.get().strip()
        dept_id = self.dept_entry.get().strip()
        if not name:
            return False, "Tên chức vụ không được để trống"
        if not dept_id:
            return False, "Mã phòng không được để trống"
        try:
            dept_id_int = int(dept_id)
            if dept_id_int <= 0:
                return False, "Mã phòng phải là số dương"
        except ValueError:
            return False, "Mã phòng phải là số"
        if len(name) > 50:
            return False, "Tên chức vụ không được vượt quá 50 ký tự"
        return True, None

class AddPositionDialog(BasePositionDialog):
    def __init__(self, parent, save_callback):
        super().__init__(parent, "Thêm Chức Vụ Mới")
        self.save_callback = save_callback

    def on_save(self):
        valid, message = self.validate_inputs()
        if not valid:
            messagebox.showerror("Lỗi Nhập Liệu", message)
            return
        try:
            ma_chuc_vu = self.id_entry.get().strip()
            if not ma_chuc_vu.isdigit():
                raise ValueError("Mã chức vụ phải là số.")
            ten_chuc_vu = self.name_entry.get().strip()
            ma_phong = int(self.dept_entry.get().strip())
            self.save_callback(ma_chuc_vu, ma_phong, ten_chuc_vu)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

class EditPositionDialog(BasePositionDialog):
    def __init__(self, parent, position, save_callback):
        super().__init__(parent, "Sửa Chức Vụ")
        self.position = position
        self.save_callback = save_callback
        self.id_entry.insert(0, str(position.ma_chuc_vu))
        self.id_entry.configure(state="readonly")
        self.name_entry.insert(0, str(position.ten_chuc_vu) if position.ten_chuc_vu is not None else "")
        self.dept_entry.insert(0, str(position.ma_phong) if position.ma_phong is not None else "")

    def on_save(self):
        valid, message = self.validate_inputs()
        if not valid:
            messagebox.showerror("Lỗi Nhập Liệu", message)
            return
        try:
            name = self.name_entry.get().strip()
            dept_id = int(self.dept_entry.get().strip())
            entry_id = int(self.id_entry.get().strip())
            self.save_callback(entry_id, dept_id, name)
            self.destroy()
        except ValueError:
            messagebox.showerror("Lỗi", "Mã chức vụ và mã phòng phải là số nguyên")

class ViewPositionDialog(BasePositionDialog):
    def __init__(self, parent, position):
        super().__init__(parent, "Chi Tiết Chức Vụ")
        self.id_entry.insert(0, position.ma_chuc_vu)
        self.id_entry.configure(state="readonly")
        self.name_entry.insert(0, position.ten_chuc_vu)
        self.name_entry.configure(state="readonly")
        self.dept_entry.insert(0, str(position.ma_phong))
        self.dept_entry.configure(state="readonly")
        self.save_btn.destroy()
        self.cancel_btn.configure(text="Đóng")

    def on_save(self):
        pass