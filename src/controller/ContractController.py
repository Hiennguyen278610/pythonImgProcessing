from src.service.ContractService import ContractService

class ContractController:
    def __init__(self):
        self.service = ContractService()
    
    def getAll(self):
        return self.service.getAll()
    
    def getByID(self, contract_id):
        return self.service.getContractByID(contract_id)
    
    def searchByName(self, term):
        # Giả sử tìm kiếm theo term (vì không có phương thức tìm kiếm cụ thể)
        return self.service.getAll()
    
    def create(self, contract_data):
        return self.service.createContract(contract_data)
    
    def update(self, contract_id, contract_data):
        return self.service.updateContract(contract_id, contract_data)
    
    def delete(self, contract_id):
        return self.service.deleteContract(contract_id)