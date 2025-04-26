import os
import shutil
import time
from customtkinter import *
from src.view.colorVariable import *
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from functools import partial
from src.utils.viewExtention import *
from src.utils.timeConvert import *
from src.controller.PositionController import PositionController
from src.controller.DepartmentController import DepartmentController
from tkinter import filedialog
from PIL import Image
from customtkinter import CTkImage

textConfig = {
    "font": ("Arial", 13, "normal"),
    "text_color": "black"
}

class EmployeeDialog(CTkToplevel):
    def __init__(self, master, controller, mode="view", employee=None, callback=None):
        """
        Dialog đa năng cho nhân viên
        
        mode: "view" (xem), "edit" (sửa), "add" (thêm)
        employee: Đối tượng nhân viên (None nếu thêm mới)
        callback: Hàm callback sau khi lưu thành công
        """
        super().__init__(master)
        self.controller = controller
        self.mode = mode
        self.employee = employee
        self.position = PositionController().getAll()
        self.department = DepartmentController().getAll()
        self.callback = callback
        self.image_data = None
        
        
        self.setupDialog()
        self.createWidgets()
        
        # Load dữ liệu nếu ở chế độ edit hoặc view
        if self.employee:
            self.loadEmployeeData()
            
        if self.mode == "view":
            self.disableControls()
            
        # Tự động chọn input đầu tiên trong form (nếu không ở chế độ xem)
        if self.mode != "view":
            self.nameEntry.focus_set()
        # Hiển thị dialog (modal)
        self.grab_set()
        
    def setupDialog(self):
        title_texts = {
            "view": "Xem chi tiết nhân viên",
            "edit": "Chỉnh sửa thông tin nhân viên",
            "add": "Thêm nhân viên mới"
        }
        self.title(title_texts.get(self.mode, "Nhân viên"))
        width, height, x, y = getCenterInit(self, 660, 605)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        
    def onClickBrowse(self, widget=None):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        filepath = filedialog.askopenfilename(title="Chọn ảnh", filetypes=filetypes)
        if not filepath:
            return
        self.set_image_button(filepath)
        self.selected_image_path = filepath

    def set_image_button(self, img_path=None):
        # Xóa widget cũ nếu có
        if hasattr(self, 'imgButton') and self.imgButton:
            self.imgButton.grid_forget()
        if hasattr(self, 'browseFile') and self.browseFile:
            self.browseFile.grid_forget()
        w, h = 308, 316
        if img_path:
            img = Image.open(img_path)
            img.thumbnail((w, h), Image.LANCZOS)
            ctk_img = CTkImage(light_image=img, dark_image=img, size=(w, h))
            self.imgButton = CTkButton(self.fromLayout, image=ctk_img, text="", command=lambda: self.onClickBrowse(self.imgButton), width=w, height=h, fg_color="white", border_color="black", border_width=2, hover_color=None)
            self.imgButton.image = ctk_img
        else:
            self.imgButton = CTkButton(self.fromLayout, text="+ Thêm ảnh", command=lambda: self.onClickBrowse(self.imgButton), width=w, height=h, fg_color="white", border_color="black", border_width=2, font=("Arial", 20, "bold"), text_color="black",hover_color=None)
        self.imgButton.grid(row=1, column=0, rowspan=5, columnspan=6, padx=10, pady=10, sticky="nsew")
        if self.mode == "view":
            self.imgButton.configure(state="disabled")

    def save_image_to_resource(self, img_path):
        if not img_path:
            print("Chưa chọn ảnh!")
            return None
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir, os.pardir))
        print(f"Project root directory: {project_root}")
        print(f"Image path: {img_path}")  # In ra đường dẫn ảnh thực tế
        resource_dir = os.path.join(project_root, "Resources", "faceImg")
        os.makedirs(resource_dir, exist_ok=True)
        
        ext = os.path.splitext(img_path)[1]
        filename = f"img_{int(time.time())}{ext}"
        dest_path = os.path.join(resource_dir, filename)

        shutil.copy(img_path, dest_path)
        print(f"Đã lưu ảnh vào: {dest_path}")
        return os.path.relpath(dest_path, project_root)
    
    def createWidgets(self):
        self.body = CTkFrame(self)
        self.body.pack(fill="both", expand=True)
        
        self.fromLayout = CTkFrame(self.body, fg_color="white")
        self.fromLayout.pack(fill="both", expand=True)
        self.fromLayout.grid_propagate(False) 
        for i in range(12):
            self.fromLayout.grid_columnconfigure(i, weight=1)
        for i in range(11):
            self.fromLayout.grid_rowconfigure(i, weight=1)

        self.infoLabel = CTkLabel(self.fromLayout, text="THÔNG TIN CÁ NHÂN", font=("Arial", 14, "bold"), text_color="black", **configFrame())
        self.infoLabel.grid(row=0, column=0, rowspan=1, columnspan=12, sticky="nsew")

        self.set_image_button()

        self.nameLabel = CTkLabel(self.fromLayout, text="Họ và tên:", **textConfig, **configFrame())
        self.nameLabel.grid(row=1, column=6, rowspan=1, columnspan=1, sticky="nse")

        self.bodLabel = CTkLabel(self.fromLayout, text="Ngày sinh:", **textConfig, **configFrame())
        self.bodLabel.grid(row=2, column=6, rowspan=1, columnspan=1, sticky="nse")

        self.genderLabel = CTkLabel(self.fromLayout, text="Giới tính:", **textConfig, **configFrame())
        self.genderLabel.grid(row=3, column=6, rowspan=1, columnspan=1, sticky="nse")

        self.phoneLabel = CTkLabel(self.fromLayout, text="Số điện thoại:", **textConfig, **configFrame())
        self.phoneLabel.grid(row=4, column=6, rowspan=1, columnspan=1, sticky="nse")

        self.adressLabel = CTkLabel(self.fromLayout, text="Địa chỉ:", **textConfig, **configFrame())
        self.adressLabel.grid(row=5, column=6, rowspan=1, columnspan=1, sticky="nse")

        self.nameEntry = CTkEntry(self.fromLayout, height=30)
        self.nameEntry.grid(row=1, column=7, rowspan=1, columnspan=5, padx=5, pady=2, sticky="ew")

        self.bodEntry = DateEntry(self.fromLayout, height=30, date_pattern='yyyy-MM-dd', state="readonly")
        self.bodEntry.grid(row=2, column=7, rowspan=1, columnspan=5, padx=5, pady=2, sticky="ew")

        self.genderEntry = CTkFrame(self.fromLayout, fg_color="transparent", **configFrame())
        self.genderEntry.grid(row=3, column=7, rowspan=1, columnspan=5, padx=5, pady=2, sticky="ew")
        self.genderEntry.grid_columnconfigure((0, 1), weight=1)
        
        self.genderValue = StringVar(value="nam")
        self.maleOption = CTkRadioButton(self.genderEntry, text="Nam", text_color="black", variable=self.genderValue, value="nam")
        self.maleOption.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)

        self.femaleOption = CTkRadioButton(self.genderEntry, text="Nữ", text_color="black", variable=self.genderValue, value="nu")
        self.femaleOption.grid(row=0, column=1, sticky="nsew", padx=5, pady=2)
        

        self.phoneEntry = CTkEntry(self.fromLayout, height=30)
        self.phoneEntry.grid(row=4, column=7, rowspan=1, columnspan=5, padx=5, pady=2, sticky="ew")

        self.addressEntry = CTkEntry(self.fromLayout, height=30)
        self.addressEntry.grid(row=5, column=7, rowspan=1, columnspan=5, padx=5, pady=2, sticky="ew")

        self.staffLabel = CTkLabel(self.fromLayout, text="THÔNG TIN NGHIỆP VỤ", font=("Arial", 14, "bold"), text_color="black", **configFrame())
        self.staffLabel.grid(row=6, column=0, rowspan=1, columnspan=12, sticky="nsew")

        self.managerLabel = CTkLabel(self.fromLayout, text="Người quản lý:", **textConfig, **configFrame())
        self.managerLabel.grid(row=7, column=0, rowspan=1, columnspan=4, sticky="nse")

        managers = convertDataComboBox(self.department, "ten_phong", "ma_truong_phong")
        self.managerEntry = CTkComboBox(self.fromLayout, height=30, values=list(managers.keys()), state="readonly")
        self.managerEntry.grid(row=7, column=4, rowspan=1, columnspan=7, padx=5, pady=2, sticky="ew")
        self.managerEntry.set(list(managers.keys())[0])

        self.positonLabel = CTkLabel(self.fromLayout, text="Chức vụ:", **textConfig, **configFrame())
        self.positonLabel.grid(row=8, column=0, rowspan=1, columnspan=4, sticky="nse")

        positions = convertDataComboBox(self.position, "ten_chuc_vu", "ma_chuc_vu")
        self.positionEntry = CTkComboBox(self.fromLayout, height=30, values=list(positions.keys()), state="readonly")
        self.positionEntry.grid(row=8, column=4, rowspan=1, columnspan=7, padx=5, pady=2, sticky="ew")
        self.positionEntry.set(list(positions.keys())[0])

        self.startDateLabel = CTkLabel(self.fromLayout, text="Ngày vào làm:", **textConfig, **configFrame())
        self.startDateLabel.grid(row=9, column=0, rowspan=1, columnspan=4, sticky="nse")
        
        self.startDateEntry = DateEntry(self.fromLayout, height=30, date_pattern='yyyy-MM-dd', state="readonly")
        self.startDateEntry.grid(row=9, column=4, rowspan=1, columnspan=7, padx=5, pady=2, sticky="ew")

        self.confirmBtn = CTkButton(self.fromLayout, text="Xác nhận", fg_color="transparent", 
            border_color="black", border_width=2, hover_color="cyan", text_color="black", command=self.saveEmployee)
        self.confirmBtn.grid(row=10, column=6, rowspan=1, columnspan=6, padx=20, pady=20, sticky="nsew")

        self.closeDialogBtn = CTkButton(self.fromLayout, text="Đóng", fg_color="transparent", 
            border_color="black", border_width=2, hover_color="cyan", text_color="black", command=self.destroy)
        self.closeDialogBtn.grid(row=10, column=0, rowspan=1, columnspan=6, padx=20, pady=20, sticky="nsew")
    
    def loadEmployeeData(self):
        if not self.employee:
            return
        
        self.nameEntry.insert(0, self.employee.ho_ten_nhan_vien or "")
        self.bodEntry.set_date(convertToDate(self.employee.ngay_sinh))
        self.genderValue.set(self.employee.gioi_tinh or "nam")
        self.phoneEntry.insert(0, self.employee.so_dien_thoai or "")
        self.addressEntry.insert(0, self.employee.dia_chi or "")
        
        managers = convertDataComboBox(self.department, "ten_phong", "ma_truong_phong")
        thismanager = [key for key, value in managers.items() if value == self.employee.ma_ngql]
        if thismanager:
            self.managerEntry.set(thismanager[0])
        
        positions = convertDataComboBox(self.position, "ten_chuc_vu", "ma_chuc_vu")
        thispos = [key for key, value in positions.items() if value == self.employee.ma_chuc_vu]
        if thispos:
            self.positionEntry.set(thispos[0])
        
        self.startDateEntry.set_date(convertToDate(self.employee.ngay_vao_lam))
        
        # Tải ảnh của nhân viên nếu có
        if hasattr(self.employee, 'url_image') and self.employee.url_image:
            try:
                # Lấy đường dẫn đầy đủ của ảnh
                script_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir, os.pardir))
                img_path = os.path.join(project_root, self.employee.url_image)
                
                if os.path.exists(img_path):
                    print(f"Đang tải ảnh từ: {img_path}")
                    # Lưu đường dẫn ảnh để sử dụng sau này
                    self.selected_image_path = img_path
                    
                    # Hiển thị ảnh
                    self.set_image_button(img_path)
            except Exception as e:
                print(f"Lỗi khi tải ảnh: {str(e)}")
        else:
            self.set_image_button()
    
    def disableControls(self):
        self.nameEntry.configure(state="disabled", fg_color="white", text_color="black", border_width=0)
        if hasattr(self, 'imgButton') and self.imgButton:
            self.imgButton.configure(state="disabled", text="")
        self.bodEntry.configure(state="disabled")
        self.phoneEntry.configure(state="disabled", fg_color="white", text_color="black", border_width=0)
        self.addressEntry.configure(state="disabled", fg_color="white", text_color="black", border_width=0)
        self.managerEntry.configure(state="disabled", fg_color="white", text_color="black", border_width=0)
        self.positionEntry.configure(state="disabled", fg_color="white", text_color="black", border_width=0)
        self.startDateEntry.configure(state="disabled")
        self.maleOption.configure(state="disabled")
        self.femaleOption.configure(state="disabled")
        self.confirmBtn.configure(state="disabled", fg_color="grey")
    
    def saveEmployee(self):
        if not self.validateForm():
            return
            
        try:
            managers = convertDataComboBox(self.department, "ten_phong", "ma_truong_phong")
            managerName = self.managerEntry.get()
            managerID = managers.get(managerName)

            positions = convertDataComboBox(self.position, "ten_chuc_vu", "ma_chuc_vu")
            positionName = self.positionEntry.get()
            positionID = positions.get(positionName)
            
            url_image = ''
            if hasattr(self, 'selected_image_path') and self.selected_image_path:
                # Truyền đường dẫn ảnh trực tiếp, không phải đối tượng
                url_image = self.save_image_to_resource(self.selected_image_path) or ''
                print(f"URL ảnh sau khi lưu: {url_image}")

            employeeData = {
                'ho_ten_nhan_vien': self.nameEntry.get().strip(),
                'ngay_sinh': self.bodEntry.get().strip(),
                'gioi_tinh': self.genderValue.get(),
                'so_dien_thoai': self.phoneEntry.get().strip(),
                'dia_chi': self.addressEntry.get().strip(),
                'ma_ngql': managerID, 
                'ma_chuc_vu': positionID, 
                'ngay_vao_lam': self.startDateEntry.get().strip(),
                'url_image': url_image
            }
            
            if self.mode == "add":
                self.controller.create(employeeData)
                message = "Thêm nhân viên thành công!"
            else:
                result = self.controller.update(self.employee.ma_nhan_vien, employeeData)
                message = "Cập nhật thông tin nhân viên thành công!"
                
            # Hiển thị thông báo thành công
            CTkMessagebox(title="Thành công", message=message, icon="check")
            
            # Gọi callback nếu có
            if self.callback:
                self.callback()
            self.after_idle(self.destroy)
                
        except Exception as e:
            CTkMessagebox(title="Lỗi", message=f"Không thể lưu dữ liệu: {str(e)}", icon="cancel")
    
    def validateForm(self):
        """Kiểm tra dữ liệu hợp lệ trước khi lưu"""
        # Họ tên
        if not self.nameEntry.get().strip():
            CTkMessagebox(title="Lỗi", message="Họ tên không được để trống!", icon="cancel")
            self.nameEntry.focus_set()
            return False
            
        # Số điện thoại
        phone = self.phoneEntry.get().strip()
        if not phone:
            CTkMessagebox(title="Lỗi", message="Số điện thoại không được để trống!", icon="cancel")
            self.phoneEntry.focus_set()
            return False
            
        if not phone.isdigit() or len(phone) != 10 or not phone.startswith('0'):
            CTkMessagebox(title="Lỗi", message="Số điện thoại phải có 10 chữ số và bắt đầu bằng số 0!", icon="cancel")
            self.phoneEntry.focus_set()
            return False
            
        # Địa chỉ
        if not self.addressEntry.get().strip():
            CTkMessagebox(title="Lỗi", message="Địa chỉ không được để trống!", icon="cancel")
            self.addressEntry.focus_set()
            return False
        return True
