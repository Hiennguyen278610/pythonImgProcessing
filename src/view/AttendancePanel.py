import customtkinter
import calendar
import datetime


from src.controller.DepartmentController import DepartmentController
from src.controller.EmployeeController import EmployeeController
from src.controller.PositionController import PositionController
from src.utils.viewExtention import getCenterInit
from src.controller.AttendanceController import AttendanceController
from src.view.colorVariable import Midnight_Navy, Ocean_Blue, Ice_Mist, fg_color, red_Calendar, yellow_Calendar, \
    green_Calendar
from src.view.component.toolbar.FilterToolbar import FilterToolbar
from src.view.dialog.checkAttendanceDialog import CheckAttendanceDialog


class AttendancePanel(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=Midnight_Navy)
        self.controllerEmpoyee = EmployeeController()
        self.controllerPosition = PositionController()
        self.controllerAttendance = AttendanceController()
        self.controllerDepartment = DepartmentController()
        self.master = master

        self.employeeList = self.controllerEmpoyee.getAll()

        self.leftFrame = customtkinter.CTkFrame(self, fg_color=Midnight_Navy, width=400, height=710)
        self.rightFrame = customtkinter.CTkFrame(self, fg_color=Midnight_Navy, width=580, height=710, corner_radius=8)
        self.searchToolbar = FilterToolbar(
            self,
            searchFields=[
                {"label": "Mã nhân viên", "field": "ma_nhan_vien"},
                {"label": "Tên nhân viên", "field": "ho_ten_nhan_vien"}
            ],
            searchCallback=self.search_employees,
            resetCallback=self.reset_search,
            fg_color=Ice_Mist,
            corner_radius=8
        )
        # self.filterTool = FilterToolbar(self.,searchFields=search_fields,searchCallback=self.onSearch,resetCallback=self.onReset)
        self.searchToolbar.place(x=10, y=10)

        self.titleEmployee = customtkinter.CTkLabel(self.rightFrame, fg_color=Ocean_Blue, text="", text_color="white",
                                                    width=560, height=40, corner_radius=8)
        self.titleEmployee.place(x=10, y=60)
        self.canlendar = customtkinter.CTkFrame(self.rightFrame, fg_color=Ocean_Blue, width=560, height=590)
        self.canlendar.place(x=10, y=110)
        self.headerCalendar = customtkinter.CTkFrame(self.canlendar, fg_color=Ocean_Blue, width=540, height=40)
        self.headerCalendar.place(x=10, y=0)
        self.bodyCalendar = customtkinter.CTkFrame(self.canlendar, fg_color=Ocean_Blue, width=540, height=540)
        self.bodyCalendar.place(x=10, y=40)

        self.leftFrame.place(x=0, y=0)
        self.rightFrame.place(x=400, y=0)

        self.checkAttendance = None
        self.currentEmployee = None

        self.initList()

    def initList(self):
        headers = ["Mã nhân viên", "Tên"]
        headerText = f"{headers[0]:<40} {headers[1]:<40}"
        headerLabel = customtkinter.CTkLabel(self.leftFrame, text=headerText, fg_color=Ocean_Blue, text_color="white", width=380, height=40, corner_radius=8)
        headerLabel.place(x=10, y=60)

        self.scrollFrame = customtkinter.CTkScrollableFrame(self.leftFrame, fg_color=Midnight_Navy, width=360, height=580)
        self.scrollFrame.place(x=10, y=110)

        self.populate_employee_list(self.employeeList)

    def populate_employee_list(self, employees):
        # Clear
        for widget in self.scrollFrame.winfo_children():
            widget.destroy()

        for employee in employees:
            department = self.controllerDepartment.getById(
                self.controllerPosition.getById(employee.ma_chuc_vu).ma_phong
            )
            text = f"{employee.ma_nhan_vien:>5} {employee.ho_ten_nhan_vien:^40}"
            button = customtkinter.CTkButton(
                self.scrollFrame,
                text=text,
                fg_color=fg_color,
                text_color="white",
                width=380,
                height=40,
                corner_radius=8,
                font=("Consolas", 13),
                command=lambda emp=employee: self.initCalendar(emp),
                border_width=1,
                border_color=fg_color,
            )
            button.pack()

    def search_employees(self, field, keyword):
        filtered_employees = []

        if not keyword:
            filtered_employees = self.employeeList
        else:
            keyword = keyword.lower()

            for employee in self.employeeList:
                if field == "ma_nhan_vien":
                    # Convert ID to string for search
                    if str(employee.ma_nhan_vien).lower().find(keyword) != -1:
                        filtered_employees.append(employee)

                elif field == "ho_ten_nhan_vien":
                    if employee.ho_ten_nhan_vien.lower().find(keyword) != -1:
                        filtered_employees.append(employee)

                elif field == "ten_phong":
                    department = self.controllerDepartment.getById(
                        self.controllerPosition.getById(employee.ma_chuc_vu).ma_phong
                    )
                    if department.ten_phong.lower().find(keyword) != -1:
                        filtered_employees.append(employee)

        # Update danh sach
        self.populate_employee_list(filtered_employees)

    def reset_search(self):
        # Reset
        self.populate_employee_list(self.employeeList)



    def initCalendar(self, employee):
        self.titleEmployee.configure(text=employee.ho_ten_nhan_vien)
        self.canlendar.destroy()
        self.canlendar = customtkinter.CTkFrame(self.rightFrame, fg_color=Ocean_Blue, width=560, height=590)
        self.canlendar.place(x=10, y=110)
        self.headerCalendar = customtkinter.CTkFrame(self.canlendar, fg_color=Ocean_Blue, width=540, height=40)
        self.headerCalendar.place(x=10, y=0)
        self.bodyCalendar = customtkinter.CTkFrame(self.canlendar, fg_color=Ocean_Blue, width=540, height=540)
        self.bodyCalendar.place(x=10, y=40)
        self.listAttendace = self.controllerAttendance.getAttendanceOfEmployee(employee)
        self.listDay = [day.ngay_cham_cong for day in self.listAttendace]
        self.currentEmployee = employee
        years = [str(year) for year in self.controllerAttendance.getAttendanceYear(employee)]
        if years:
            self.comboBoxMonth = customtkinter.CTkComboBox(self.headerCalendar, fg_color=Midnight_Navy, text_color="white", dropdown_text_color="white", dropdown_fg_color=Ocean_Blue, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], width=120, height=30, command=self.onMonthOrYearChange)
            self.comboBoxMonth.place(x=10, y=10)
            self.comboBoxYear = customtkinter.CTkComboBox(self.headerCalendar, values=years, fg_color=Midnight_Navy, text_color="white", dropdown_fg_color="white", dropdown_text_color="black", width=120, height=30, command=self.onMonthOrYearChange)
            self.comboBoxYear.place(x=140, y=10)
            self.initDay(int(self.comboBoxYear.get()), int(self.comboBoxMonth.get()), self.listDay)

    def onMonthOrYearChange(self, _=None):
        self.bodyCalendar.destroy()
        self.bodyCalendar = customtkinter.CTkFrame(self.canlendar, fg_color=Ocean_Blue, width=610, height=540)
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
        width = 70
        height= 70
        for day in range(num_days):
            weekday_name = weekdays[col]
            label_text = f"{day + 1} {weekday_name}"
            da = datetime.date(year, month, day + 1)
            day_label = customtkinter.CTkButton(self.bodyCalendar, text=label_text, width=width, height=height,
                                                fg_color=red_Calendar, text_color="black", corner_radius=0, border_width=1,border_color=fg_color,
                                                command=lambda d = da: self.openCheckAttendanceDialog(d, self.currentEmployee))
            if da in ld:
                index = ld.index(da)
                if self.listAttendace[index].gio_ra:
                    day_label.configure(fg_color=green_Calendar)
                else:
                    day_label.configure(fg_color=yellow_Calendar)
            day_label.place(x=x + col*width, y=y + row*height)
            col = col + 1
            if col > 6:
                col = 0
                row += 1

    def openCheckAttendanceDialog(self, day, employee):
        attendanced = None
        for att in self.listAttendace:
            if att.ngay_cham_cong == day:
                attendanced = att
                break
        if self.checkAttendance is not None:
            self.checkAttendance.destroy()
        self.checkAttendance = CheckAttendanceDialog(self, attendanced, employee, day)
        self.checkAttendance.grab_set()
        self.checkAttendance.focus()