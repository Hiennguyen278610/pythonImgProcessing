from tkinter import Image

import customtkinter
import cv2
import os
from customtkinter import CTkImage
from PIL import Image, ImageDraw
from face_recognition import face_locations
from src.model.repository.PositionRespository import PositionRespository
from src.utils.viewExtention import getCenterInit
from src.controller.AttendanceController import AttendanceController
from src.service.AttendanceService import AttendanceService

class AttendancePanel(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = AttendanceController()
        self.controller.loadData()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=2)

        self.rightFrame = customtkinter.CTkFrame(self, fg_color="white")
        self.rightFrame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.rightFrame.grid_rowconfigure(0, weight=9)  # Ảnh chiếm 40%
        self.rightFrame.grid_rowconfigure(1, weight=1)  # Tên
        self.rightFrame.grid_rowconfigure(2, weight=1)  # Mã NV
        self.rightFrame.grid_rowconfigure(3, weight=1)  # Chức vụ
        self.rightFrame.grid_rowconfigure(4, weight=1)  # Phòng ban
        self.rightFrame.grid_rowconfigure(5, weight=1)
        self.rightFrame.grid_columnconfigure(0, weight=1)

        self.leftFrame = customtkinter.CTkFrame(self, fg_color="white")
        self.leftFrame.grid(row=0, column=0, columnspan = 2, padx=10, pady=10, sticky="nsew")
        self.leftFrame.grid_rowconfigure(0, weight=1)
        self.leftFrame.grid_columnconfigure(0, weight=1)

        self.video = customtkinter.CTkLabel(self.leftFrame, fg_color="black", text = "", corner_radius=16)
        self.video.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.imgEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="black", text = "", corner_radius=16)
        self.imgEmployee.grid(row=0, column=0, rowspan=1, padx=5, pady=5, sticky="nsew")

        self.nameEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="black", text = "Tên: ", corner_radius=16)
        self.nameEmployee.grid(row=1, column=0, rowspan=1, padx=5, pady=5, sticky="nsew")

        self.idEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="black", text = "Mã nhân viên: ", corner_radius=16)
        self.idEmployee.grid(row = 2, column = 0, rowspan = 1, padx = 10, pady = 5, sticky = "nsew")

        self.positionEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="black", text = "Chức vụ: ", corner_radius=16)
        self.positionEmployee.grid(row = 3, column = 0, rowspan = 1, padx = 10, pady = 5, sticky = "nsew")

        self.departmentEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="black", text="Phòng ban: ", corner_radius=16)
        self.departmentEmployee.grid(row=4, column=0, rowspan=1, padx=10, pady=5, sticky="nsew")

        self.confirm = customtkinter.CTkFrame(self.rightFrame, fg_color="black")
        self.confirm.grid(row=5, column=0, rowspan=1, padx=10, pady=5, sticky="nsew")
        self.cap= cv2.VideoCapture(0)
        self.recognize()

    def recognize(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        employee = self.controller.attendance(frame)
        frame = self.rectangelFace(frame)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(rgb_frame)
        img_pil = img_pil.resize((self.video.winfo_width(), self.video.winfo_height()))
        ctk_img = CTkImage(light_image=img_pil, size=(760, 570))
        self.video.configure(image=ctk_img, text="")
        self.video.image = ctk_img
        if employee != None:
            self.display_information(employee)
            self.video.configure(image=ctk_img, text="")
            self.video.image = ctk_img
        else: self.after(10, self.recognize)

    def rectangelFace(self, frame):
        face_locations = self.controller.getLocation(frame)
        for i, (top, right, bottom, left) in enumerate(face_locations):
            top, right, bottom, left = top, right, bottom , left
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 200), 2)
        return frame

    def display_information(self, employee):
        image_path = os.path.join("src", "..", "Resources", employee.url_image)
        if os.path.exists(image_path):
            pil_image = Image.open(image_path)
            ctk_img = CTkImage(pil_image, size=(150, 150))
            self.imgEmployee.configure(image=ctk_img, text="")
            self.imgEmployee.image = ctk_img
        self.nameEmployee.configure(text=f"Tên: {employee.ho_ten_nhan_vien}")
        self.idEmployee.configure(text=f"Mã nhân viên: {employee.ma_nhan_vien}")
        # position = PositionRespository.findById(employee.roleID)
        # self.positionEmployee.configure(f"Chức vụ: {position.ma_chuc_vu}")
        # self.departmentEmployee.configure(f"Phòng ban: {position.ma_phong}")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        w, h, x, y = getCenterInit(self, 1280, 720)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = AttendancePanel(master=self, width=w, height=h)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

app = App()
app.mainloop()