from src.model.entity.EmployeeEntity import Employee
from src.model.repository.EmployeeRespository import EmployeeRepository

class EmployeeService:
    def __init__(self):
        self.repository = EmployeeRepository()
    
    def getAll(self):
        return self.repository.findAll()
    
    def getEmployeeByID(self, ma_nhan_vien):
        return self.repository.findByID(ma_nhan_vien)
    
    def searchEmployeesByName(self, ho_ten_nhan_vien):
        return self.repository.findByName(ho_ten_nhan_vien)
    
    def createEmployee(self, employeeData):
        employee = Employee(
            ma_nhan_vien=None,  # ID sẽ được cơ sở dữ liệu tự sinh
            ma_ngql=employeeData.get('ma_ngql'),
            ma_chuc_vu=employeeData.get('ma_chuc_vu'),
            ho_ten_nhan_vien=employeeData.get('ho_ten_nhan_vien'),
            ngay_sinh=employeeData.get('ngay_sinh'),
            so_dien_thoai=employeeData.get('so_dien_thoai'),
            dia_chi=employeeData.get('dia_chi'),
            gioi_tinh=employeeData.get('gioi_tinh'),
            ngay_vao_lam=employeeData.get('ngay_vao_lam'),
            url_image=employeeData.get('url_image')
        )

        self.validEmployee(employee)
        return self.repository.save(employee)
    
    def updateEmployee(self, ma_nhan_vien, employeeData):
        # Kiểm tra xem nhân viên có tồn tại không
        existEmployee = self.repository.findByID(ma_nhan_vien)
        if not existEmployee:
            raise ValueError(f"Nhân viên có mã {ma_nhan_vien} không tồn tại.")
        
        if 'ma_ngql' in employeeData:
            existEmployee.ma_ngql = employeeData.get('ma_ngql')
        if 'ma_chuc_vu' in employeeData:
            existEmployee.ma_chuc_vu = employeeData.get('ma_chuc_vu')
        if 'ho_ten_nhan_vien' in employeeData:
            existEmployee.ho_ten_nhan_vien = employeeData.get('ho_ten_nhan_vien')
        if 'ngay_sinh' in employeeData:
            existEmployee.ngay_sinh = employeeData.get('ngay_sinh')
        if 'so_dien_thoai' in employeeData:
            existEmployee.so_dien_thoai = employeeData.get('so_dien_thoai')
        if 'dia_chi' in employeeData:
            existEmployee.dia_chi = employeeData.get('dia_chi')
        if 'gioi_tinh' in employeeData:
            existEmployee.gioi_tinh = employeeData.get('gioi_tinh')
        if 'ngay_vao_lam' in employeeData:
            existEmployee.ngay_vao_lam = employeeData.get('ngay_vao_lam')
        if 'url_image' in employeeData:
            existEmployee.url_image = employeeData.get('url_image')
        
        self.validEmployee(existEmployee)
        return self.repository.save(existEmployee)
    
    def deleteEmployee(self, ma_nhan_vien):
        existEmployee = self.repository.findByID(ma_nhan_vien)
        if not existEmployee:
            raise ValueError(f"Nhân viên có mã {ma_nhan_vien} không tồn tại.")
        return self.repository.delete(ma_nhan_vien)
    
    # Kiểm tra các trường bắt buộc
    def validEmployee(self, employee):
        if not employee.ho_ten_nhan_vien or not employee.ho_ten_nhan_vien.strip():
            raise ValueError("Tên nhân viên không được để trống.")
        
        if not employee.so_dien_thoai or not employee.so_dien_thoai.strip():
            raise ValueError("Số điện thoại không được để trống.")
        
        if not employee.so_dien_thoai.isdigit() or len(employee.so_dien_thoai) != 10 or not employee.so_dien_thoai.startswith('0'):
            raise ValueError("Số điện thoại phải là chữ số, có độ dài là 10 và bắt đầu bằng số 0.")
        
        return True