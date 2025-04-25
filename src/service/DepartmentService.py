from src.model.entity.DepartmentEntity import Department
from src.model.repository.DepartmentRespository import DepartmentRespository
from src.model.repository.EmployeeRespository import EmployeeRepository
from src.model.repository.PositionRespository import PositionRespository
import re
from tkinter import messagebox



class DepartmentService:
    def __init__(self):
        self.repository = DepartmentRespository()
        self.position_repository = PositionRespository()

    def findAll(self):
        return self.repository.findAll()

    def save(self, department):
        return self.repository.save(department)

    def findById(self, ma_phong):
        return self.repository.findById(ma_phong)

    def search(self, search_text, keyword):
        return self.repository.search(search_text, keyword)

    def createDepartment(self, departmentData):
        department = Department(
            ma_phong=None,
            ma_truong_phong=departmentData.get('ma_truong_phong'),
            ten_phong=departmentData.get('ten_phong')
        )
        self.validateDepartment(department)
        return self.repository.save(department)

    def updateDepartment(self, ma_phong, departmentData):
        existDepartment = self.repository.findById(ma_phong)
        if not existDepartment:
            raise ValueError(f"Phòng ban có mã {ma_phong} không tồn tại.")

        if 'ma_truong_phong' in departmentData:
            existDepartment.ma_truong_phong = departmentData.get('ma_truong_phong')
        if 'ten_phong' in departmentData:
            existDepartment.ten_phong = departmentData.get('ten_phong')

        self.validateDepartment(existDepartment)
        return self.repository.save(existDepartment)

    def deleteDepartment(self, ma_phong):
        existDepartment = self.repository.findById(ma_phong)
        if not existDepartment:
            raise ValueError(f"Phòng ban có mã {ma_phong} không tồn tại.")

        # Xóa các chức vụ thuộc phòng ban này (bao gồm các phân công liên quan)
        self.position_repository.deleteByDepartmentId(ma_phong)

        # Sau khi không còn phụ thuộc, xóa phòng ban
        return self.repository.delete(ma_phong)

    def validateDepartment(self, department):
        ten_phong = department.ten_phong.strip() if department.ten_phong else ''

        if not ten_phong:
            raise ValueError("Tên phòng ban không được để trống.")

        if len(ten_phong) > 50:
            raise ValueError("Tên phòng ban không được vượt quá 50 ký tự.")

        if re.search(r'[^a-zA-ZÀ-ỹ\s]', ten_phong):
            raise ValueError("Tên phòng ban không được chứa ký tự đặc biệt hoặc số.")

        return True
