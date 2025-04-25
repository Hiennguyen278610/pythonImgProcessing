from customtkinter import *
from src.utils.viewExtention import *
from src.view.AttendancePanel import AttendancePanel
from src.view.DepartmentPanel import DepartmentPanel
from src.view.colorVariable import *
from src.view.component.TaskBar import TaskBar
from src.view.EmployeePanel import EmployeePanel
from src.view.ContractPanel import ContractPanel
from src.view.PositionPanel import PositionPanel
from src.controller.PositionController import PositionController

def mainFrame(parent_app=None):
    mainPanel = CTk()
    mainPanel.title("Ứng dụng chấm công")

    w, h, x, y = getCenterInit(mainPanel, 1280, 720)
    mainPanel.geometry(f"{w}x{h}+{x}+{y}")

    body = CTkFrame(mainPanel)
    body.place(relwidth=1, relheight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_columnconfigure(0, weight=1)
    body.grid_columnconfigure(1, weight=9)

    left = CTkFrame(body, fg_color=Sky_Harbor)
    left.grid(row=0, column=0, sticky="nsew")
    left.grid_rowconfigure(0, weight=1)
    left.grid_rowconfigure(1, weight=9)
    left.grid_columnconfigure(0, weight=1)

    leftTop = CTkFrame(left, fg_color=Ocean_Blue, height=50)
    leftTop.grid(row=0, column=0, sticky="nsew")

    title_label = CTkLabel(
        leftTop,
        text="Staff Manager",
        font=("Arial", 16, "bold"),
        text_color=textClr
    )
    title_label.pack(padx=10, pady=10)

    leftBottom = TaskBar(left, fg_color=Sky_Harbor)
    leftBottom.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    right = CTkFrame(body, fg_color=Midnight_Navy)
    right.grid(row=0, column=1, sticky="nsew")
    right.grid_rowconfigure(0, weight=1)
    right.grid_columnconfigure(0, weight=1)

    current_panel = None

    def on_entity_selected(key, entity_class):
        nonlocal current_panel
        if current_panel:
            current_panel.grid_forget()

        if key == "employee":
            current_panel = EmployeePanel(right)
        elif key == "contract":
            current_panel = ContractPanel(right)
        elif key == "position":
            current_panel = PositionPanel(right, PositionController())
        elif key == "department":
            current_panel = DepartmentPanel(right)
        elif key == "attendance":
            current_panel = AttendancePanel(right)

        if current_panel:
            current_panel.grid(row=0, column=0, sticky="nsew")

    leftBottom.add_entity("Nhân viên", "employee", EmployeePanel)
    leftBottom.add_entity("Hợp đồng", "contract", ContractPanel)
    leftBottom.add_entity("Chức vụ", "position", PositionPanel)
    leftBottom.add_entity("Phòng ban", "department", DepartmentPanel)
    leftBottom.add_entity("Điểm danh", "attendance", AttendancePanel)

    leftBottom.entity_callback = on_entity_selected

    # Đóng mainPanel và mở lại login nếu có
    def on_close():
        if parent_app:
            parent_app.deiconify()
        mainPanel.destroy()

    mainPanel.protocol("WM_DELETE_WINDOW", on_close)

    return mainPanel
