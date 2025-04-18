from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkFrame
from src.model.entity.PositionEntity import Position


class BasePositionDialog(CTkToplevel):


    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)

        self.transient(parent)
        self.after_idle(self.grab_set)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_rowconfigure(3, weight=1)

        CTkLabel(main_frame, text="Tên chức vụ:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.name_entry = CTkEntry(
            main_frame, placeholder_text="Nhập tên chức vụ"
        )
        self.name_entry.grid(
            row=0, column=1, padx=10, pady=10, sticky="ew"
        )

        # Department ID
        CTkLabel(main_frame, text="Mã phòng:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        self.dept_entry = CTkEntry(
            main_frame, placeholder_text="Nhập mã phòng"
        )
        self.dept_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew"
        )

        button_frame = CTkFrame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.save_btn = CTkButton(
            button_frame, text="Lưu", command=self.on_save
        )
        self.save_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.cancel_btn = CTkButton(
            button_frame, text="Hủy", command=self.destroy
        )
        self.cancel_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.name_entry.focus_set()

    def on_save(self):
        pass

    def validate_inputs(self):
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

        # Check name length
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
            from tkinter import messagebox
            messagebox.showerror("Lỗi Nhập Liệu", message)
            return

        name = self.name_entry.get().strip()
        dept_id = int(self.dept_entry.get().strip())

        self.save_callback(dept_id, name)
        self.destroy()


class EditPositionDialog(BasePositionDialog):

    def __init__(self, parent, position, save_callback):
        """Initialize edit dialog"""
        super().__init__(parent, "Sửa Chức Vụ")
        self.position = position
        self.save_callback = save_callback

        # Populate fields
        self.name_entry.insert(0, position.ten_chuc_vu)
        self.dept_entry.insert(0, str(position.ma_phong))

    def on_save(self):
        valid, message = self.validate_inputs()
        if not valid:
            from tkinter import messagebox
            messagebox.showerror("Lỗi Nhập Liệu", message)
            return

        name = self.name_entry.get().strip()
        dept_id = int(self.dept_entry.get().strip())

        self.save_callback(self.position.ma_chuc_vu, dept_id, name)
        self.destroy()


class ViewPositionDialog(BasePositionDialog):

    def __init__(self, parent, position):
        super().__init__(parent, "Chi Tiết Chức Vụ")

        self.name_entry.insert(0, position.ten_chuc_vu)
        self.name_entry.configure(state="readonly")

        self.dept_entry.insert(0, str(position.ma_phong))
        self.dept_entry.configure(state="readonly")

        # Change button to "Close" only
        self.save_btn.destroy()
        self.cancel_btn.configure(text="Đóng")

    def on_save(self):
        pass