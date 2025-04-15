from datetime import datetime

class Employee:
    def __init__(self, employeeID: int, managerID: int, roleID: int, name: str, dob: datetime, 
                 phone: str, address: str, gender: str, startDate: datetime, urlImage: str):
        self.employeeID = employeeID
        self.managerID = managerID
        self.roleID = roleID
        self.name = name
        self.dob = dob
        self.phone = phone
        self.address = address
        self.gender = gender
        self.startDate = startDate
        self.urlImage = urlImage