from src.model.entity.ContractEntity import Contract
from src.model.repository.ContractRespository import ContractRepository

class ContractService:
    def __init__(self):
        self.repository = ContractRepository()
    
    def getAll(self):
        return self.repository.findAll()
    
    def getContractByID(self, ma_hop_dong):
        return self.repository.findByID(ma_hop_dong)
    
    def getContractsByEmployeeID(self, ma_nhan_vien):
        return self.repository.findByEmployeeID(ma_nhan_vien)
    
    def createContract(self, contractData):
        contract = Contract(
            ma_hop_dong=None,  # ID sẽ được cơ sở dữ liệu tự sinh
            ma_nhan_vien=contractData.get('ma_nhan_vien'),
            thoi_han=contractData.get('thoi_han'),
            ngay_ky=contractData.get('ngay_ky'),
            muc_luong=contractData.get('muc_luong')
        )
        self.validContract(contract)
        return self.repository.save(contract)
    
    def updateContract(self, ma_hop_dong, contractData):
        existingContract = self.repository.findByID(ma_hop_dong)
        if not existingContract:
            raise ValueError(f"Hợp đồng có mã {ma_hop_dong} không tồn tại.")
        
        if 'ma_nhan_vien' in contractData:
            existingContract.ma_nhan_vien = contractData.get('ma_nhan_vien')
        if 'thoi_han' in contractData:
            existingContract.thoi_han = contractData.get('thoi_han')
        if 'ngay_ky' in contractData:
            existingContract.ngay_ky = contractData.get('ngay_ky')
        if 'muc_luong' in contractData:
            existingContract.muc_luong = contractData.get('muc_luong')
        
        self.validContract(existingContract)
        return self.repository.save(existingContract)
    
    def deleteContract(self, ma_hop_dong):
        existingContract = self.repository.findByID(ma_hop_dong)
        if not existingContract:
            raise ValueError(f"Hợp đồng có mã {ma_hop_dong} không tồn tại.")
        return self.repository.delete(ma_hop_dong)
    
    # Kiểm tra các trường bắt buộc
    def validContract(self, contract):
        if not contract.ma_nhan_vien:
            raise ValueError("Mã nhân viên không được để trống.")
        if not contract.thoi_han or not contract.thoi_han.strip():
            raise ValueError("Thời hạn hợp đồng không được để trống.")
        if not contract.ngay_ky:
            raise ValueError("Ngày ký không được để trống.")
        if not contract.muc_luong or contract.muc_luong <= 0:
            raise ValueError("Mức lương phải là số dương.")
        return True