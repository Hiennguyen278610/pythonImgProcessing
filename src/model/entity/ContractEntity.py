from datetime import datetime

class Contract:
    def __init__(self, contractID: int, employeeID: int, term: str, signingDate: datetime, salary: float):
        self.contractID = contractID
        self.employeeID = employeeID
        self.term = term
        self.signingDate = signingDate
        self.salary = salary
        
    def __str__(self):
        return f"Contract [ID={self.contractID}, EmployeeID={self.employeeID}, Term={self.term}, SigningDate={self.signingDate.strftime('%Y-%m-%d')}, Salary={self.salary}]"