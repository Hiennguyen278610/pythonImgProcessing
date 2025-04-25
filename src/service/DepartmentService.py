from src.model.entity.DepartmentEntity import Department
from src.model.repository.DepartmentRespository import DepartmentRespository
import re
from tkinter import messagebox

class DepartmentService:
    def __init__(self):
        self.repository = DepartmentRespository()

    def findAll(self):
        return self.repository.findAll()

    def save(self,department):
        return self.repository.save(department)

    def findById(self, ma_phong):
        return self.repository.findById(ma_phong)

    def search(self, search_text,keyword):
        return self.repository.search(search_text, keyword)

    def createDepartment(self, departmentData):
        department = Department(
            ma_phong=None,  # ID sẽ được cơ sở dữ liệu tự sinh
            ma_truong_phong=departmentData.get('ma_truong_phong'),
            ten_phong=departmentData.get('ten_phong')
        )
        
        self.validDepartment(department)
        return self.repository.save(department)
    
    def updateDepartment(self, ma_phong, departmentData):
        existDepartment = self.repository.findById(ma_phong)
        if not existDepartment:
            raise ValueError(f"Phòng ban có mã {ma_phong} không tồn tại.")
        
        if 'ma_truong_phong' in departmentData:
            existDepartment.ma_truong_phong = departmentData.get('ma_truong_phong')
        if 'ten_phong' in departmentData:
            existDepartment.ten_phong = departmentData.get('ten_phong')
        
        self.validDepartment(existDepartment)
        return self.repository.save(existDepartment)
    
    def deleteDepartment(self, ma_phong):
        existDepartment = self.repository.findById(ma_phong)
        if not existDepartment:
            raise ValueError(f"Phòng ban có mã {ma_phong} không tồn tại.")
        return self.repository.delete(ma_phong)

    def validDepartment(self, department):
        ten_phong = department.ten_phong

        if not ten_phong or not ten_phong.strip():
            messagebox.showwarning("Cảnh bảo","tên phòng không được rỗng")
            raise ValueError("Tên phòng ban không được để trống.")

        if len(ten_phong) > 50:
            messagebox.showwarning("Cảnh báo","Tên phòng không được vượt quá 50 kí tự")
            raise ValueError("Tên phòng ban không được vượt quá 50 ký tự.")

        if re.search(r'[^a-zA-ZÀ-ỹ\s]', ten_phong):
            messagebox.showwarning("Cảnh báo","tên phòng không được số hoặc kí tự đặc biệt")
            raise ValueError("Tên phòng ban không được chứa ký tự đặc biệt hoặc số.")

        return True
