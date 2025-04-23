from tkinter import Image

import customtkinter
import cv2
import os
from customtkinter import CTkImage
from PIL import Image, ImageDraw
from face_recognition import face_locations

from src.controller.DepartmentController import DepartmentController
from src.controller.PositionController import PositionController
from src.model.repository.PositionRespository import PositionRespository
from src.utils.viewExtention import getCenterInit
from src.controller.AttendanceController import AttendanceController
from src.service.AttendanceService import AttendanceService

class FaceRegconiton(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = AttendanceController()
        self.controller.loadData()
        self.controllerPosition = PositionController()
        self.controllerDepartment = DepartmentController()

        self.rightFrame = customtkinter.CTkFrame(self, fg_color="blue", width=380, height=680)
        self.rightFrame.place(x=860, y=0)

        self.leftFrame = customtkinter.CTkFrame(self, fg_color="blue", width=860,height=680)
        self.leftFrame.place(x=0, y=0,)

        self.video = customtkinter.CTkLabel(self.leftFrame, fg_color="white", text = "", corner_radius=16, width=840, height=660)
        self.video.place(x=10, y=10,)

        self.imgEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="white", text = "", corner_radius=16, width=250, height = 250)
        self.nameEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="white", text = "Tên: ", corner_radius=16, text_color="black", width = 340, height = 50)
        self.idEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="white", text = "Mã nhân viên: ", corner_radius=16, text_color="black", width = 340, height = 50)
        self.positionEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="white", text = "Chức vụ: ", corner_radius=16, text_color="black", width = 340, height = 50)
        self.departmentEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="white", text="Phòng ban: ", corner_radius=16, text_color="black", width = 340, height = 50)

        self.imgEmployee.place(x = 65, y = 10,)
        self.nameEmployee.place(x= 20, y=270,)
        self.idEmployee.place(x=20, y=330)
        self.positionEmployee.place(x=20, y=390)
        self.departmentEmployee.place(x=20, y=450)

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
        if hasattr(self, "frame_counter"):
            self.frame_counter += 1
        else:
            self.frame_counter = 0
        if employee != None and self.frame_counter >= 5:
            self.display_information(employee)
            self.confirmBox(frame, employee)
            #TODO: xác nhận sau đó gọi hàm database ở đây
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
            ctk_img = CTkImage(pil_image, size=(200, 200))
            self.imgEmployee.configure(image=ctk_img, text="")
            self.imgEmployee.image = ctk_img
        self.nameEmployee.configure(text=f"Tên: {employee.ho_ten_nhan_vien}")
        self.idEmployee.configure(text=f"Mã nhân viên: {employee.ma_nhan_vien}")
        self.positionEmployee.configure(text=f"Chức vụ: {self.controllerPosition.getById(employee.ma_chuc_vu).ten_chuc_vu}")
        self.departmentEmployee.configure(text=f"Phòng ban: {self.controllerDepartment.getById(self.controllerPosition.getById(employee.ma_chuc_vu).ma_phong).ten_phong}")

    def confirmBox(self, frame, employee):
        self.buttonYes = customtkinter.CTkButton(self.rightFrame, text="Điểm danh", fg_color="green", text_color="white", width=150, height=50, command=lambda: self.buttonYesActive(frame, employee))
        self.buttonNo = customtkinter.CTkButton(self.rightFrame, text="Thử lại", fg_color="red", text_color="white", width=150, height=50, command=lambda: self.tryAgain())
        self.buttonYes.place(x=20, y=510,)
        self.buttonNo.place(x=210, y=510)

    def tryAgain(self):
        self.buttonYes.destroy()
        self.buttonNo.destroy()
        self.after(10, self.recognize)

    def buttonYesActive(self, frame, employee):
        self.controller.checkIn(frame, employee.ma_nhan_vien)
        self.destroy()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        w, h, x, y = getCenterInit(self, 1280, 720)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = FaceRegconiton(master=self, width=w, height=h)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# app = App()
# app.mainloop()
