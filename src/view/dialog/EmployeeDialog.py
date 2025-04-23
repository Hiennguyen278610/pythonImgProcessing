from customtkinter import *
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from datetime import datetime

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
        self.callback = callback
        self.image_data = None
        
        # Cấu hình dialog
        self.setupDialog()
        
        # Tạo giao diện
        self.createWidgets()
        
        # Load dữ liệu nếu ở chế độ edit hoặc view
        if self.employee:
            self.loadEmployeeData()
        
        # Disable controls trong chế độ view
        if self.mode == "view":
            self.disableControls()
            
        # Tự động chọn input đầu tiên trong form (nếu không ở chế độ xem)
        if self.mode != "view":
            self.name_entry.focus_set()
            
        # Hiển thị dialog (modal)
        self.grab_set()
        
    def setupDialog(self):
        # Thiết lập tiêu đề
        title_texts = {
            "view": "Xem chi tiết nhân viên",
            "edit": "Chỉnh sửa thông tin nhân viên",
            "add": "Thêm nhân viên mới"
        }
        self.title(title_texts.get(self.mode, "Nhân viên"))
        
        # Kích thước và vị trí
        width, height = 720, 600
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
    
    def createWidgets(self):
        # Main container
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form layout
        self.form_frame = CTkFrame(self.main_frame)
        self.form_frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        title_texts = {
            "view": "THÔNG TIN CHI TIẾT NHÂN VIÊN",
            "edit": "CHỈNH SỬA THÔNG TIN NHÂN VIÊN",
            "add": "THÊM NHÂN VIÊN MỚI"
        }
        CTkLabel(self.form_frame, text=title_texts.get(self.mode), 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        # Tạo form chính
        self.content_frame = CTkFrame(self.form_frame)
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Layout grid
        for i in range(2):
            self.content_frame.grid_columnconfigure(i, weight=1)
        
        # === Thông tin cá nhân ===
        row = 0
        CTkLabel(self.content_frame, text="THÔNG TIN CÁ NHÂN", 
                font=("Arial", 14, "bold")).grid(row=row, column=0, columnspan=2, 
                sticky="w", pady=(5, 10))
        
        # Họ tên
        row += 1
        CTkLabel(self.content_frame, text="Họ tên:").grid(row=row, column=0, 
                sticky="e", padx=10, pady=8)
        self.name_entry = CTkEntry(self.content_frame, width=250)
        self.name_entry.grid(row=row, column=1, sticky="w", padx=10)
        
        # Ngày sinh
        row += 1
        CTkLabel(self.content_frame, text="Ngày sinh:").grid(row=row, column=0, 
                sticky="e", padx=10, pady=8)
        self.birthdate_entry = CTkEntry(self.content_frame, width=250, 
                placeholder_text="YYYY-MM-DD")
        self.birthdate_entry.grid(row=row, column=1, sticky="w", padx=10)
        
        # Giới tính
        row += 1
        CTkLabel(self.content_frame, text="Giới tính:").grid(row=row, column=0, 
                sticky="e", padx=10, pady=8)
        self.gender_frame = CTkFrame(self.content_frame, fg_color="transparent")
        self.gender_frame.grid(row=row, column=1, sticky="w", padx=10)
        self.gender_var = StringVar(value="nam")
        self.male_radio = CTkRadioButton(self.gender_frame, text="Nam", 
                variable=self.gender_var, value="nam")
        self.male_radio.pack(side="left", padx=(0, 20))
        self.female_radio = CTkRadioButton(self.gender_frame, text="Nữ", 
                variable=self.gender_var, value="nu")
        self.female_radio.pack(side="left")
        
        # Số điện thoại
        row += 1
        CTkLabel(self.content_frame, text="Số điện thoại:").grid(row=row, column=0, 
                sticky="e", padx=10, pady=8)
        self.phone_entry = CTkEntry(self.content_frame, width=250)
        self.phone_entry.grid(row=row, column=1, sticky="w", padx=10)
        
        # Địa chỉ
        row += 1
        CTkLabel(self.content_frame, text="Địa chỉ:").grid(row=row, column=0, 
                sticky="e", padx=10, pady=8)
        self.address_entry = CTkEntry(self.content_frame, width=250)
        self.address_entry.grid(row=row, column=1, sticky="w", padx=10)
        
        # === Thông tin công việc ===
        row += 1
        CTkLabel(self.content_frame, text="THÔNG TIN CÔNG VIỆC", 
                font=("Arial", 14, "bold")).grid(row=row, column=0, columnspan=2, 
                sticky="w", pady=(20, 10))
        
        # Chức vụ
        row += 1
        CTkLabel(self.content_frame, text="Chức vụ:").grid(row=row, column=0, 
                sticky="e", padx=10, pady=8)
        self.position_combo = CTkComboBox(self.content_frame, width=250)
        self.position_combo.grid(row=row, column=1, sticky="w", padx=10)
        
        # Người quản lý
        row += 1
        CTkLabel(self.content_frame, text="Người quản lý:").grid(row=row, column=0, 
                sticky="e", padx=10, pady=8)
        self.manager_combo = CTkComboBox(self.content_frame, width=250)
        self.manager_combo.grid(row=row, column=1, sticky="w", padx=10)
        
        # Ngày vào làm
        row += 1
        CTkLabel(self.content_frame, text="Ngày vào làm:").grid(row=row, column=0, 
                sticky="e", padx=10, pady=8)
        self.start_date_entry = CTkEntry(self.content_frame, width=250, 
                placeholder_text="YYYY-MM-DD")
        self.start_date_entry.grid(row=row, column=1, sticky="w", padx=10)
        
        # === Ảnh đại diện ===
        row += 1
        CTkLabel(self.content_frame, text="ẢNH ĐẠI DIỆN", 
                font=("Arial", 14, "bold")).grid(row=row, column=0, columnspan=2, 
                sticky="w", pady=(20, 10))
        
        # Image frame
        row += 1
        self.image_frame = CTkFrame(self.content_frame)
        self.image_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=8)
        
        # Image preview
        self.image_path = StringVar()
        self.image_label = CTkLabel(self.image_frame, text="[Ảnh đại diện]", width=150, height=150)
        self.image_label.pack(side="left", padx=10)
        
        # Image buttons
        self.image_buttons = CTkFrame(self.image_frame, fg_color="transparent")
        self.image_buttons.pack(side="left", padx=10)
        
        self.browse_button = CTkButton(self.image_buttons, text="Chọn ảnh", 
                command=self.browseImage)
        self.browse_button.pack(pady=5)
        
        self.image_path_label = CTkLabel(self.image_buttons, text="Chưa chọn ảnh", wraplength=200)
        self.image_path_label.pack(pady=5)
        
        # === Buttons ===
        self.button_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", pady=15)
        
        # Tùy chọn nút dựa trên chế độ
        if self.mode == "view":
            self.close_button = CTkButton(self.button_frame, text="Đóng", 
                    command=self.destroy, width=100)
            self.close_button.pack(side="right", padx=10)
        else:
            self.save_button = CTkButton(self.button_frame, text="Lưu", 
                    command=self.saveEmployee, width=100)
            self.save_button.pack(side="right", padx=10)
            self.cancel_button = CTkButton(self.button_frame, text="Hủy", 
                    command=self.destroy, width=100)
            self.cancel_button.pack(side="right", padx=10)
    
    def browseImage(self):
        """Mở dialog chọn file ảnh"""
        file_types = [("Image files", "*.jpg *.jpeg *.png *.gif")]
        file_path = filedialog.askopenfilename(title="Chọn ảnh nhân viên", filetypes=file_types)
        
        if file_path:
            self.image_path.set(file_path)
            self.image_path_label.configure(text=os.path.basename(file_path))
            # TODO: Hiển thị ảnh preview
    
    def loadEmployeeData(self):
        """Load dữ liệu nhân viên vào form"""
        if not self.employee:
            return
        
        # Thông tin cá nhân
        self.name_entry.insert(0, self.employee.ho_ten_nhan_vien or "")
        self.birthdate_entry.insert(0, str(self.employee.ngay_sinh) if self.employee.ngay_sinh else "")
        self.gender_var.set(self.employee.gioi_tinh or "nam")
        self.phone_entry.insert(0, self.employee.so_dien_thoai or "")
        self.address_entry.insert(0, self.employee.dia_chi or "")
        
        # Thông tin công việc
        # TODO: Load dữ liệu chức vụ và manager vào combobox
        
        self.start_date_entry.insert(0, str(self.employee.ngay_vao_lam) if self.employee.ngay_vao_lam else "")
        
        # Ảnh đại diện
        if self.employee.url_image:
            self.image_path.set(self.employee.url_image)
            self.image_path_label.configure(text=os.path.basename(self.employee.url_image))
            # TODO: Hiển thị ảnh preview
    
    def disableControls(self):
        """Disable tất cả input controls trong chế độ xem"""
        for widget in [self.name_entry, self.birthdate_entry, self.phone_entry, 
                      self.address_entry, self.position_combo, self.manager_combo,
                      self.start_date_entry, self.browse_button]:
            widget.configure(state="disabled")
        
        self.male_radio.configure(state="disabled") 
        self.female_radio.configure(state="disabled")
    
    def saveEmployee(self):
        """Lưu thông tin nhân viên"""
        if not self.validateForm():
            return
            
        try:
            # Thu thập dữ liệu từ form
            employee_data = {
                'ho_ten_nhan_vien': self.name_entry.get().strip(),
                'ngay_sinh': self.birthdate_entry.get().strip(),
                'gioi_tinh': self.gender_var.get(),
                'so_dien_thoai': self.phone_entry.get().strip(),
                'dia_chi': self.address_entry.get().strip(),
                'ma_ngql': None,  # TODO: Xử lý lấy ID từ combobox
                'ma_chuc_vu': None,  # TODO: Xử lý lấy ID từ combobox
                'ngay_vao_lam': self.start_date_entry.get().strip(),
                'url_image': self.image_path.get() or 'faceImg\\default.jpg',
                'trang_thai': 'active'
            }
            
            # Thực hiện thêm hoặc cập nhật
            if self.mode == "add":
                result = self.controller.create(employee_data)
                message = "Thêm nhân viên thành công!"
            else:  # edit mode
                result = self.controller.update(self.employee.ma_nhan_vien, employee_data)
                message = "Cập nhật thông tin nhân viên thành công!"
                
            # Hiển thị thông báo thành công
            CTkMessagebox(title="Thành công", message=message, icon="check")
            
            # Gọi callback nếu có
            if self.callback:
                self.callback()
                
            # Đóng dialog
            self.destroy()
                
        except Exception as e:
            CTkMessagebox(title="Lỗi", message=f"Không thể lưu dữ liệu: {str(e)}", icon="cancel")
    
    def validateForm(self):
        """Kiểm tra dữ liệu hợp lệ trước khi lưu"""
        # Họ tên
        if not self.name_entry.get().strip():
            CTkMessagebox(title="Lỗi", message="Họ tên không được để trống!", icon="cancel")
            self.name_entry.focus_set()
            return False
            
        # Số điện thoại
        phone = self.phone_entry.get().strip()
        if not phone:
            CTkMessagebox(title="Lỗi", message="Số điện thoại không được để trống!", icon="cancel")
            self.phone_entry.focus_set()
            return False
            
        if not phone.isdigit() or len(phone) != 10 or not phone.startswith('0'):
            CTkMessagebox(title="Lỗi", message="Số điện thoại phải có 10 chữ số và bắt đầu bằng số 0!", icon="cancel")
            self.phone_entry.focus_set()
            return False
            
        # Địa chỉ
        if not self.address_entry.get().strip():
            CTkMessagebox(title="Lỗi", message="Địa chỉ không được để trống!", icon="cancel")
            self.address_entry.focus_set() 
            return False
            
        # TODO: Kiểm tra định dạng ngày tháng
        
        return True