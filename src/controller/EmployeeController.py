from src.service.EmployeeService import EmployeeService

class EmployeeController:
    def __init__(self):
        self.service = EmployeeService()
    
    def getAll(self):
        return self.service.getAll()
    
    def getByID(self, employee_id):
        return self.service.getEmployeeByID(employee_id)
    
    def searchByName(self, name):
        return self.service.searchEmployeesByName(name)
    
    def create(self, employee_data):
        return self.service.createEmployee(employee_data)
    
    def update(self, employee_id, employee_data):
        return self.service.updateEmployee(employee_id, employee_data)
    
    def delete(self, employee_id):
        try:
            result = self.service.deleteEmployee(employee_id)
            return result
        except Exception as e:
            raise Exception(f"Không thể xóa nhân viên: {str(e)}")