from tkinter import Image

import customtkinter
import cv2
import os
from customtkinter import CTkImage
from PIL import Image, ImageDraw
from face_recognition import face_locations
from numpy.ma.core import filled
from src.controller.EmployeeController import EmployeeController
from src.controller.PositionController import PositionController
from src.utils.viewExtention import getCenterInit
from src.controller.AttendanceController import AttendanceController
from src.service.AttendanceService import AttendanceService

class AttendancePanel(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controllerEmpoyee = EmployeeController()
        self.controllerPosition = PositionController()
        self.controllerAttendance = AttendanceController()

        self.leftFrame = customtkinter.CTkFrame(self, fg_color="blue", width=532, height=492)
        self.rightFrame = customtkinter.CTkFrame(self, fg_color="blue", width=650, height=492)
        self.titleEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="white", text="", text_color="black", width=630, height=40, corner_radius=8)
        self.titleEmployee.place(x=10, y=10)
        self.canlendar = customtkinter.CTkFrame(self.rightFrame, fg_color="white", width=630, height=422)
        self.canlendar.place(x=10, y=60)

        self.leftFrame.place(x=0, y=0)
        self.rightFrame.place(x=542, y=0)

        self.initList()

    def initList(self):
        headers = ["Mã nhân viên", "Tên", "Phòng"]
        headerText = f"{headers[0]:<40} {headers[1]:<40} {headers[2]:>30}"
        headerLabel = customtkinter.CTkLabel(self.leftFrame, text=headerText, fg_color="white", text_color="black", width=512, height=40, corner_radius=8)
        headerLabel.place(x=10, y=10)

        scrollFrame = customtkinter.CTkScrollableFrame(self.leftFrame, width=492, height=412)
        scrollFrame.place(x=10, y=60)

        employeeList = self.controllerEmpoyee.getAll()
        for employee in employeeList:
            text = f"{employee.ma_nhan_vien:>5} {employee.ho_ten_nhan_vien:^40} {self.controllerPosition.getPhong(employee.ma_chuc_vu):^20}"
            button = customtkinter.CTkButton(scrollFrame, text=text, fg_color="white", text_color="black", width = 492, height=40, corner_radius=0, font=("Consolas", 13), command=lambda emp = employee: self.initCalendar(emp))
            button.pack()

    def initCalendar(self, employee):
        self.titleEmployee.configure(text=employee.ho_ten_nhan_vien)
        years = [str(year) for year in self.controllerAttendance.getAttendanceYear(employee)]
        comboBoxMonth = customtkinter.CTkComboBox(self.canlendar, fg_color="white", text_color="black", dropdown_text_color="black", dropdown_fg_color="white", values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], width=120, height=30)
        comboBoxMonth.place(x=10, y=10)
        comboBoxYear = customtkinter.CTkComboBox(self.canlendar, values=years, fg_color="white", text_color="black", dropdown_fg_color="white", dropdown_text_color="black", width=120, height=30)
        comboBoxYear.place(x=140, y=10)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        w, h, x, y = getCenterInit(self, 1192, 492)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = AttendancePanel(master=self, width=1192, height=492)
        self.my_frame.grid(row=0, column=0,sticky="nsew")

app = App()
app.mainloop()
