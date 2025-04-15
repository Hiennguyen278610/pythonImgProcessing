from src.model.entity.ContractEntity import Contract
from src.model.repository.ContractRespository import ContractRepository

class ContractService:
    def __init__(self):
        self.repository = ContractRepository()
    
    def getAll(self):
        return self.repository.findAll()
    
    def getContractByID(self, contractID):
        return self.repository.findByID(contractID)
    
    def getContractsByEmployeeID(self, employeeID):
        return self.repository.findByEmployeeID(employeeID)
    
    def createContract(self, contractData):
        contract = Contract(
            contractID=None,  # ID sẽ được cơ sở dữ liệu tự sinh
            employeeID=contractData.get('employeeID'),
            term=contractData.get('term'),
            signingDate=contractData.get('signingDate'),
            salary=contractData.get('salary')
        )
        self.validContract(contract)
        return self.repository.save(contract)
    
    def updateContract(self, contractID, contractData):
        existingContract = self.repository.findByID(contractID)
        if not existingContract:
            raise ValueError(f"This contract with ID {contractID} does not exist.")
        
        if 'employeeID' in contractData:
            existingContract.employeeID = contractData.get('employeeID')
        if 'term' in contractData:
            existingContract.term = contractData.get('term')
        if 'signingDate' in contractData:
            existingContract.signingDate = contractData.get('signingDate')
        if 'salary' in contractData:
            existingContract.salary = contractData.get('salary')
        
        self.validContract(existingContract)
        return self.repository.save(existingContract)
    
    def deleteContract(self, contractID):
        existingContract = self.repository.findByID(contractID)
        if not existingContract:
            raise ValueError(f"This contract with ID {contractID} does not exist.")
        return self.repository.delete(contractID)
    
    # Kiểm tra các trường bắt buộc
    def validContract(self, contract):
        if not contract.employeeID:
            raise ValueError("Employee ID cannot be empty.")
        if not contract.term or not contract.term.strip():
            raise ValueError("Contract term cannot be empty.")
        if not contract.signingDate:
            raise ValueError("Signing date cannot be empty.")
        if not contract.salary or contract.salary <= 0:
            raise ValueError("Salary must be a positive number.")
        return True