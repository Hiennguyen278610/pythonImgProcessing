import customtkinter
import calendar
import datetime
from src.controller.DepartmentController import DepartmentController
from src.controller.EmployeeController import EmployeeController
from src.controller.PositionController import PositionController
from src.utils.viewExtention import getCenterInit
from src.controller.AttendanceController import AttendanceController

class AttendancePanel(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controllerEmpoyee = EmployeeController()
        self.controllerPosition = PositionController()
        self.controllerAttendance = AttendanceController()
        self.controllerDepartment = DepartmentController()

        self.leftFrame = customtkinter.CTkFrame(self, fg_color="blue", width=532, height=492)
        self.rightFrame = customtkinter.CTkFrame(self, fg_color="blue", width=650, height=492)
        self.titleEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color="white", text="", text_color="black", width=630, height=40, corner_radius=8)
        self.titleEmployee.place(x=10, y=10)
        self.canlendar = customtkinter.CTkFrame(self.rightFrame, fg_color="white", width=630, height=422)
        self.canlendar.place(x=10, y=60)
        self.headerCalendar = customtkinter.CTkFrame(self.canlendar, fg_color="white", width=610, height=40)
        self.headerCalendar.place(x=10, y=0)
        self.bodyCalendar = customtkinter.CTkFrame(self.canlendar, fg_color="white", width=610, height=380)
        self.bodyCalendar.place(x=10, y=40)

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
            text = f"{employee.ma_nhan_vien:>5} {employee.ho_ten_nhan_vien:^40} {self.controllerDepartment.getById(self.controllerPosition.getById(employee.ma_chuc_vu).ma_phong).ten_phong:^20}"
            button = customtkinter.CTkButton(scrollFrame, text=text, fg_color="white", text_color="black", width = 492, height=40, corner_radius=0, font=("Consolas", 13), command=lambda emp = employee: self.initCalendar(emp))
            button.pack()

    def initCalendar(self, employee):
        self.titleEmployee.configure(text=employee.ho_ten_nhan_vien)
        self.canlendar.destroy()
        self.canlendar = customtkinter.CTkFrame(self.rightFrame, fg_color="white", width=630, height=422)
        self.canlendar.place(x=10, y=60)
        self.headerCalendar = customtkinter.CTkFrame(self.canlendar, fg_color="white", width=610, height=40)
        self.headerCalendar.place(x=10, y=0)
        self.bodyCalendar = customtkinter.CTkFrame(self.canlendar, fg_color="white", width=610, height=380)
        self.bodyCalendar.place(x=10, y=40)
        self.listAttendace = self.controllerAttendance.getAttendanceOfEmployee(employee)
        self.listDay = [day.ngay_cham_cong for day in self.listAttendace]
        years = [str(year) for year in self.controllerAttendance.getAttendanceYear(employee)]
        if years:
            self.comboBoxMonth = customtkinter.CTkComboBox(self.headerCalendar, fg_color="white", text_color="black", dropdown_text_color="black", dropdown_fg_color="white", values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], width=120, height=30, command=self.onMonthOrYearChange)
            self.comboBoxMonth.place(x=10, y=10)
            self.comboBoxYear = customtkinter.CTkComboBox(self.headerCalendar, values=years, fg_color="white", text_color="black", dropdown_fg_color="white", dropdown_text_color="black", width=120, height=30, command=self.onMonthOrYearChange)
            self.comboBoxYear.place(x=140, y=10)
            self.initDay(int(self.comboBoxYear.get()), int(self.comboBoxMonth.get()), self.listDay)

    def onMonthOrYearChange(self, _=None):
        self.bodyCalendar.destroy()
        self.bodyCalendar = customtkinter.CTkFrame(self.canlendar, fg_color="white", width=610, height=380)
        self.bodyCalendar.place(x=10, y=40)
        year = int(self.comboBoxYear.get())
        month = int(self.comboBoxMonth.get())
        self.initDay(year, month, self.listDay)

    def initDay(self, year, month, ld):
        num_days = calendar.monthrange(year, month)[1]
        first_day_weekday = (calendar.monthrange(year, month)[0] + 1) % 7
        weekdays = ["CN", "Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy"]
        x = 30
        y = 10
        col = first_day_weekday
        row = 0
        width = 80
        height= 60
        for day in range(num_days):
            weekday_name = weekdays[col]
            label_text = f"{day + 1} {weekday_name}"
            day_label = customtkinter.CTkLabel(self.bodyCalendar, text=label_text, width=width, height=height, fg_color="red", text_color="black")
            da = datetime.date(year, month, day + 1)
            if da in ld:
                index = ld.index(da)
                if self.listAttendace[index].gio_ra:
                    day_label.configure(fg_color="green")
                else:
                    day_label.configure(fg_color="yellow")
            day_label.place(x=x + col*width, y=y + row*height)
            col = col + 1
            if col > 6:
                col = 0
                row += 1


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
