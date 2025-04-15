from src.model.entity.EmployeeEntity import Employee
from src.model.repository.EmployeeRespository import EmployeeRepository

class EmployeeService:
    def __init__(self):
        self.repository = EmployeeRepository()
    
    def getAll(self):
        return self.repository.findAll()
    
    def getEmployeeByID(self, employeeID):
        return self.repository.findByID(employeeID)
    
    def searchEmployeesByName(self, name):
        return self.repository.findByName(name)
    
    def createEmployee(self, employeeData):
        employee = Employee(
            employeeID=None,  # ID sẽ được cơ sở dữ liệu tự sinh
            managerID=employeeData.get('managerID'),
            roleID=employeeData.get('roleID'),
            name=employeeData.get('name'),
            dob=employeeData.get('dob'),
            phone=employeeData.get('phone'),
            address=employeeData.get('address'),
            gender=employeeData.get('gender'),
            startDate=employeeData.get('startDate')
        )

        self.validEmployee(employee)
        return self.repository.save(employee)
    
    def updateEmployee(self, employeeID, employeeData):
        # Kiểm tra xem nhân viên có tồn tại không
        existEmployee = self.repository.findByID(employeeID)
        if not existEmployee:
            raise ValueError(f"This {employeeID} is employee null.")
        
        # Cập nhật thông tin nhân viên
        if 'managerID' in employeeData:
            existEmployee.managerID = employeeData.get('managerID')
        if 'roleID' in employeeData:
            existEmployee.roleID = employeeData.get('roleID')
        if 'name' in employeeData:
            existEmployee.name = employeeData.get('name')
        if 'dob' in employeeData:
            existEmployee.dob = employeeData.get('dob')
        if 'phone' in employeeData:
            existEmployee.phone = employeeData.get('phone')
        if 'address' in employeeData:
            existEmployee.address = employeeData.get('address')
        if 'gender' in employeeData:
            existEmployee.gender = employeeData.get('gender')
        if 'startDate' in employeeData:
            existEmployee.startDate = employeeData.get('startDate')
        
        self.validEmployee(existEmployee)
        return self.repository.save(existEmployee)
    
    def deleteEmployee(self, employeeID):
        existEmployee = self.repository.findByID(employeeID)
        if not existEmployee:
            raise ValueError(f"This {employeeID} is employee null.")
        return self.repository.delete(employeeID)
    
    # Kiểm tra các trường bắt buộc
    def validEmployee(self, employee):
        if not employee.name or not employee.name.strip():
            raise ValueError("Employee name not null.")
        
        if not employee.phone or not employee.phone.strip():
            raise ValueError("Employee phone not null.")
        
        if not employee.phone.isdigit() and len(employee.phone == 10) and employee.phone.startswith('0'):
            raise ValueError("Employee phone just only digit, lenght phone just equal 10 and start with.")
        
        return True