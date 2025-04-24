import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import FaceRecognition
from login import loginFrame
from src.view.AttendancePanel import AttendancePanel

# Biến màu từ mã trước
primaryClr = "#6D54B5"
secondaryCrl = "#3C364C"  # Nền btn
accentClr = "#757283"  # Placeholder btn
bgClr = "#2c2736"
textClr = "#FFFFFF"
borderClr = "#000000"


class AttendanceListPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=bgClr)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            self,
            text="Danh sách chấm công\n(Dữ liệu giả lập)\n" +
                 f"Ngày: {datetime.now().strftime('%d/%m/%Y')}",
            font=("San Serif", 18, "bold"),
            text_color=textClr
        )
        label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


class HomeFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=bgClr)

        # Cấu hình lưới
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)


        title = ctk.CTkLabel(
            self,
            text="Hệ thống chấm công",
            font=("San Serif", 36, "bold"),
            text_color=textClr
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")


        button_frame = ctk.CTkFrame(self, fg_color=bgClr)
        button_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        button_frame.grid_rowconfigure(0, weight=1)

        # Nút chấm công cho nhân viên
        staff_button = ctk.CTkButton(
            button_frame,
            text="Chấm công (Nhân viên)",
            font=("San Serif", 18, "bold"),
            fg_color=primaryClr,
            text_color=textClr,
            border_spacing=10,
            command=self.open_staff_camera
        )
        staff_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Nút đăng nhập cho manager
        manager_button = ctk.CTkButton(
            button_frame,
            text="Đăng nhập (Manager)",
            font=("San Serif", 18, "bold"),
            fg_color=primaryClr,
            text_color=textClr,
            border_spacing=10,
            command=self.open_manager_login
        )
        manager_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Nút hiển thị danh sách chấm công
        attendance_button = ctk.CTkButton(
            button_frame,
            text="Danh sách chấm công",
            font=("San Serif", 18, "bold"),
            fg_color=primaryClr,
            text_color=textClr,
            border_spacing=10,
            command=self.show_attendance_list
        )
        attendance_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Biến lưu panel danh sách chấm công
        self.attendance_panel = None

    def open_staff_camera(self):
        try:
            FaceRecognition.App().mainloop()
        except Exception as e:
            CTkMessagebox(
                title="Lỗi",
                message=f"Không thể mở camera chấm công: {str(e)}"
            )

    def open_manager_login(self):
        try:
            self.master.destroy()  # Đóng frame hiện tại
            loginFrame().mainloop()  # Mở giao diện đăng nhập
        except Exception as e:
            CTkMessagebox(
                title="Lỗi",
                message=f"Không thể mở giao diện đăng nhập: {str(e)}"
            )

    def show_attendance_list(self):
        """Hiển thị danh sách chấm công"""
        try:
            if self.attendance_panel:
                self.attendance_panel.destroy()
            self.attendance_panel = AttendanceListPanel(self)
            self.attendance_panel.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        except Exception as e:
            CTkMessagebox(
                title="Lỗi",
                message=f"Không thể hiển thị danh sách chấm công: {str(e)}"
            )


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")
    root.title("Hệ thống chấm công")
    root._set_appearance_mode("dark")

    home_frame = HomeFrame(root)
    home_frame.pack(fill="both", expand=True)

    root.mainloop()