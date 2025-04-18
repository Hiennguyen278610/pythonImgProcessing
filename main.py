from customtkinter import *
from src.utils.viewExtention import *
from src.view.colorVariable import *
from src.view.component.TaskBar import TaskBar
from src.view.EmployeePanel import EmployeePanel
from src.view.ContractPanel import ContractPanel
from src.view.PositionPanel import PositionPanel
from src.controller.PositionController import PositionController

def mainFrame():
    mainPanel = CTk()
    mainPanel.title("Ứng dụng chấm công")
    
    w, h, x, y = getCenterInit(mainPanel, 1280, 720)
    mainPanel.geometry(f"{w}x{h}+{x}+{y}")
    
    body = CTkFrame(mainPanel)
    body.place(relwidth=1, relheight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_columnconfigure(0, weight=1)
    body.grid_columnconfigure(1, weight=9)
    
    left = CTkFrame(body, fg_color=bgClr)
    left.grid(row=0, column=0, sticky="nsew")
    left.grid_rowconfigure(0, weight=1)
    left.grid_rowconfigure(1, weight=9)
    left.grid_columnconfigure(0, weight=1)
    
    leftTop = CTkFrame(left, fg_color=primaryClr, height=50)
    leftTop.grid(row=0, column=0, sticky="nsew")
    
    # Tiêu đề ứng dụng
    title_label = CTkLabel(
        leftTop, 
        text="Staff Manager", 
        font=("Arial", 16, "bold"),
        text_color=textClr
    )
    title_label.pack(padx = 10, pady=10)
    
    # Tạo TaskBar có thể cuộn được
    leftBottom = TaskBar(left, fg_color=secondaryCrl)
    leftBottom.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    
    # Tạo frame cho nội dung bên phải
    right = CTkFrame(body, fg_color=bgClr)
    right.grid(row=0, column=1, sticky="nsew")
    right.grid_rowconfigure(0, weight=1)
    right.grid_columnconfigure(0, weight=1)
    
    # Biến lưu panel hiện tại
    current_panel = None
    
    # Hàm để chuyển đổi panel
    def on_entity_selected(key, entity_class):
        nonlocal current_panel
        
        # Xóa panel hiện tại nếu có
        if current_panel:
            current_panel.grid_forget()

        # Tạo panel mới dựa trên entity được chọn
        if key == "employee":
            current_panel = EmployeePanel(right)
        elif key == "contract":
            current_panel = ContractPanel(right)
        elif key == "position":
            current_panel = PositionPanel(right, PositionController())


        # Hiển thị panel mới
        if current_panel:
            current_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    # Thêm các đối tượng vào taskbar
    leftBottom.add_entity("Nhân viên", "employee", EmployeePanel)
    leftBottom.add_entity("Hợp đồng", "contract", ContractPanel)
    leftBottom.add_entity("Chức vụ", "position", PositionPanel)

    # Gán callback cho taskbar
    leftBottom.entity_callback = on_entity_selected
    
    return mainPanel

mainPanel = mainFrame()
mainPanel.mainloop()