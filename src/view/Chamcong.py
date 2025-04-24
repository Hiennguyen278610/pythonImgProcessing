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


# Hàm để căn giữa cửa sổ
def center_window(window, width, height):
    """Căn giữa cửa sổ trên màn hình desktop"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


class AttendanceListPanel(ctk.CTkFrame):
    def init(self, parent):
        super().init(parent, fg_color=bgClr)
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
            app = FaceRecognition.App()
            # Căn giữa cửa sổ camera chấm công
            app.after(100, lambda: center_window(app, 800, 600))
            app.mainloop()
        except Exception as e:
            CTkMessagebox(
                title="Lỗi",
                message=f"Không thể mở camera chấm công: {str(e)}"
            )

    def open_manager_login(self):
        try:
            self.master.destroy()  # Đóng frame hiện tại
            login_frame = loginFrame()
            # Căn giữa cửa sổ đăng nhập
            login_frame.after(100, lambda: center_window(login_frame, 800, 600))
            login_frame.mainloop()
        except Exception as e:
            CTkMessagebox(
                title="Lỗi",
                message=f"Không thể mở giao diện đăng nhập: {str(e)}"
            )

    def show_attendance_list(self):
        """Hiển thị danh sách chấm công trong cửa sổ mới"""
        try:
            attendance_window = ctk.CTkToplevel(self)
            attendance_window.title("Danh sách chấm công")
            attendance_window.withdraw()

            container = ctk.CTkFrame(attendance_window, fg_color=bgClr)
            container.pack(fill="both", expand=True)

            header = ctk.CTkFrame(container, fg_color="#3C364C", height=40)
            header.pack(fill="x", padx=0, pady=0)

            title = ctk.CTkLabel(
                header,
                text="Danh sách chấm công",
                font=("San Serif", 16, "bold"),
                text_color=textClr,
                anchor="w"
            )
            title.pack(side="left", padx=10, pady=5)

            close_button = ctk.CTkButton(
                header,
                text="X",
                width=30,
                height=30,
                fg_color=primaryClr,
                hover_color="#8A70DB",
                command=attendance_window.destroy
            )
            close_button.pack(side="right", padx=10, pady=5)

            attendance_panel = AttendancePanel(container)
            attendance_panel.pack(fill="both", expand=True, padx=0, pady=0)


            center_window(attendance_window, 980, 710)

            attendance_window.deiconify()
            attendance_window.lift()
            attendance_window.focus_force()


            attendance_window.resizable(False, False)

        except Exception as e:
            CTkMessagebox(
                title="Lỗi",
                message=f"Không thể hiển thị danh sách chấm công: {str(e)}"
            )


if __name__ == "__main__":
    root = ctk.CTk()
    # Ẩn cửa sổ chính trước khi căn giữa
    root.withdraw()
    root.title("Hệ thống chấm công")
    root._set_appearance_mode("dark")

    home_frame = HomeFrame(root)
    home_frame.pack(fill="both", expand=True)

    # Căn giữa cửa sổ chính
    center_window(root, 800, 600)

    # Hiện cửa sổ sau khi căn giữa
    root.deiconify()

    root.mainloop()