from src.model.repository.DepartmentRespository import DepartmentRespository
from src.service.DepartmentService import DepartmentService
from src.controller.EmployeeController import EmployeeController  # import controller

class DepartmentController:
    def __init__(self, employeeController=None):
        self.service = DepartmentService()
        self.employeeController = employeeController or EmployeeController()  # dùng controller

    def getAll(self):
        return self.service.findAll()

    def getAllEmployees(self):
        return self.employeeController.getAll()  # dùng hàm getAll từ EmployeeController

    def getById(self, ma_phong):
        return self.service.findById(ma_phong)

    def create(self, departmentData):
        return self.service.createDepartment(departmentData)

    def update(self, ma_phong, departmentData):
        return self.service.updateDepartment(ma_phong, departmentData)

    def delete(self, ma_phong):
        return self.service.deleteDepartment(ma_phong)

    def search(self, search_text, keyword):
        return self.service.search(search_text, keyword)
