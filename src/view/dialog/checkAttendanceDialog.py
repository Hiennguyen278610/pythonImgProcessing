import customtkinter
from pathlib import Path
from PIL import Image
from customtkinter import CTkImage
class CheckAttendanceDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, attendanced, employee, day):
        customtkinter.CTkToplevel.__init__(self, parent)
        self.geometry("1000x600")
        self.configure(fg_color="blue")
        self.header = customtkinter.CTkFrame(self, height=50, fg_color="white")
        self.header.pack(side="top", fill="x", expand="true", pady=(0, 10), padx=10)
        self.body = customtkinter.CTkFrame(self, height=540, fg_color="blue")
        self.body.pack(side="bottom", fill="both", expand="true")

        self.attendanced = attendanced
        self.employee = employee

        self.id = customtkinter.CTkLabel(self.header, height=50, fg_color="white",
                                         text = f"Mã nhân viên: {employee.ma_nhan_vien}",
                                         text_color = "black")
        self.id.pack(side = "left", fill="x", expand="true", padx=10)
        self.name = customtkinter.CTkLabel(self.header, height=50, fg_color="white",
                                           text = f"Tên: {employee.ho_ten_nhan_vien}",
                                           text_color = "black")
        self.name.pack(side = "left", fill="x", expand="true", padx=10)
        self.day = customtkinter.CTkLabel(self.header, height=50, fg_color="white",
                                          text = f"Ngày: {day.strftime("%Y-%m-%d")}",
                                          text_color = "black")
        self.day.pack(side="left", fill="x", expand="true", padx=10)

        self.checkIn = customtkinter.CTkFrame(self.body, height=530, fg_color="white")
        self.checkIn.pack(side="left", fill="x", expand="true", padx=10)
        self.checkOut = customtkinter.CTkFrame(self.body, height=530, fg_color="white")
        self.checkOut.pack(side="left", fill="x", expand="true", padx=(0, 10))
        self.timeCheckIn = customtkinter.CTkLabel(self.checkIn, height=50, fg_color="white",
                                                  text=f"Không checkin ngày {day.strftime('%Y-%m-%d')}",
                                                  text_color = "black")
        self.timeCheckIn.pack(side="top", fill="x", expand="true", padx=10)
        self.timeCheckOut = customtkinter.CTkLabel(self.checkOut, height=50, fg_color="white",
                                                   text=f"Không checkout ngày {day.strftime('%Y-%m-%d')}",
                                                   text_color = "black")
        self.timeCheckOut.pack(side="top", fill="x", expand="true", padx=10)
        self.imgCheckIn = customtkinter.CTkLabel(self.checkIn, text="", height=450)
        self.imgCheckIn.pack(side="bottom", fill="x", expand="true", padx=10, pady=10)
        self.imgCheckOut = customtkinter.CTkLabel(self.checkOut, text="", height=450)
        self.imgCheckOut.pack(side="bottom", fill="x", expand="true", padx=10, pady=10)
        if attendanced:
            self.timeCheckIn.configure(text=f"Thời gian: {str(attendanced.gio_vao)}")
            self.timeCheckOut.configure(text="Chưa checkout")
            if Path(attendanced.img_checkin).exists():
                pil_image = Image.open(Path(attendanced.img_checkin))
                ctk_img = CTkImage(pil_image, size=(400, 300))
                self.imgCheckIn.configure(image=ctk_img)
                print("Tìm thấy ảnh!")
            else:
                print("Ảnh không tồn tại:", Path(attendanced.img_checkin))
            if attendanced.gio_ra is not None:
                self.timeCheckOut.configure(text=f"Thời gian: {str(attendanced.gio_ra)}")
                pil_image = Image.open(Path(attendanced.img_checkout))
                ctk_img = CTkImage(pil_image, size=(400, 300))
                self.imgCheckOut.configure(image=ctk_img)