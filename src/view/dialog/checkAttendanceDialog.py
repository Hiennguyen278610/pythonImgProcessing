import customtkinter
from pathlib import Path
from PIL import Image
from customtkinter import CTkImage

from src.view.colorVariable import Ocean_Blue


class CheckAttendanceDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, attendanced, employee, day):
        super().__init__(parent)
        self.geometry("1000x600")
        self.configure(fg_color=Ocean_Blue)

        # Header frame
        self.header = customtkinter.CTkFrame(self, height=50, fg_color="white")
        self.header.pack(side="top", fill="x", expand=True, pady=(0, 10), padx=10)
        # Body frame
        self.body = customtkinter.CTkFrame(self, height=540, fg_color=Ocean_Blue)
        self.body.pack(side="bottom", fill="both", expand=True)

        # Store data
        self.attendanced = attendanced
        self.employee = employee

        # Employee info labels
        self.id_label = customtkinter.CTkLabel(
            self.header, height=50, fg_color="white",
            text=f"Mã nhân viên: {employee.ma_nhan_vien}", text_color="black"
        )
        self.id_label.pack(side="left", fill="x", expand=True, padx=10)
        self.name_label = customtkinter.CTkLabel(
            self.header, height=50, fg_color="white",
            text=f"Tên: {employee.ho_ten_nhan_vien}", text_color="black"
        )
        self.name_label.pack(side="left", fill="x", expand=True, padx=10)
        self.date_label = customtkinter.CTkLabel(
            self.header, height=50, fg_color="white",
            text=f"Ngày: {day.strftime('%Y-%m-%d')}", text_color="black"
        )
        self.date_label.pack(side="left", fill="x", expand=True, padx=10)

        # Check-in and check-out frames
        self.checkIn_frame = customtkinter.CTkFrame(self.body, height=530, fg_color="white")
        self.checkIn_frame.pack(side="left", fill="x", expand=True, padx=10)
        self.checkOut_frame = customtkinter.CTkFrame(self.body, height=530, fg_color="white")
        self.checkOut_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Time labels
        self.timeCheckIn = customtkinter.CTkLabel(
            self.checkIn_frame, height=50, fg_color="white",
            text=f"Không checkin ngày {day.strftime('%Y-%m-%d')}", text_color="black"
        )
        self.timeCheckIn.pack(side="top", fill="x", expand=True, padx=10)
        self.timeCheckOut = customtkinter.CTkLabel(
            self.checkOut_frame, height=50, fg_color="white",
            text=f"Không checkout ngày {day.strftime('%Y-%m-%d')}", text_color="black"
        )
        self.timeCheckOut.pack(side="top", fill="x", expand=True, padx=10)

        # Image placeholders
        self.imgCheckIn = customtkinter.CTkLabel(self.checkIn_frame, text="", height=450)
        self.imgCheckIn.pack(side="bottom", fill="x", expand=True, padx=10, pady=10)
        self.imgCheckOut = customtkinter.CTkLabel(self.checkOut_frame, text="", height=450)
        self.imgCheckOut.pack(side="bottom", fill="x", expand=True, padx=10, pady=10)

        # Determine project root for resolving paths
        project_root = Path(__file__).resolve().parents[3]

        # Populate data if available
        if attendanced:
            # Check-in time and image
            self.timeCheckIn.configure(text=f"Thời gian: {attendanced.gio_vao}")
            if attendanced.img_checkin:
                img_in_path = (project_root / attendanced.img_checkin).resolve()
                if img_in_path.exists():
                    pil_in = Image.open(img_in_path)
                    ctk_in = CTkImage(pil_in, size=(400, 300))
                    self.imgCheckIn.configure(image=ctk_in)
                else:
                    print("Không tìm thấy ảnh check-in:", img_in_path)

            # Check-out time and image
            if attendanced.gio_ra is not None:
                self.timeCheckOut.configure(text=f"Thời gian: {attendanced.gio_ra}")
                if attendanced.img_checkout:
                    img_out_path = (project_root / attendanced.img_checkout).resolve()
                    if img_out_path.exists():
                        pil_out = Image.open(img_out_path)
                        ctk_out = CTkImage(pil_out, size=(400, 300))
                        self.imgCheckOut.configure(image=ctk_out)
                    else:
                        print("Không tìm thấy ảnh check-out:", img_out_path)

        # Ensure the dialog is visible before grabbing focus
        self.update_idletasks()
        self.grab_set()
        self.focus()
