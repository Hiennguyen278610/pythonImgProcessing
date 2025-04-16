from src.model.entity.PositionEntity import Position
from src.model.repository.PositionRespository import PositionRespository

class PositionService:
    def __init__(self):
        self.repository = PositionRespository()
    
    def getAll(self):
        return self.repository.findAll()
    
    def getPositionByID(self, ma_chuc_vu):
        return self.repository.findById(ma_chuc_vu)
    
    def getPositionsByDepartment(self, ma_phong):
        return self.repository.findByDepartment(ma_phong)
    
    def createPosition(self, positionData):
        position = Position(
            ma_chuc_vu=positionData.get('ma_chuc_vu'),
            ma_phong=positionData.get('ma_phong'),
            ten_chuc_vu=positionData.get('ten_chuc_vu')
        )
        
        self.validPosition(position)
        return self.repository.save(position)
    
    def updatePosition(self, ma_chuc_vu, positionData):
        existPosition = self.repository.findById(ma_chuc_vu)
        if not existPosition:
            raise ValueError(f"Chức vụ có mã {ma_chuc_vu} không tồn tại.")
        
        if 'ma_phong' in positionData:
            existPosition.ma_phong = positionData.get('ma_phong')
        if 'ten_chuc_vu' in positionData:
            existPosition.ten_chuc_vu = positionData.get('ten_chuc_vu')
        
        self.validPosition(existPosition)
        return self.repository.save(existPosition)
    
    def deletePosition(self, ma_chuc_vu):
        existPosition = self.repository.findById(ma_chuc_vu)
        if not existPosition:
            raise ValueError(f"Chức vụ có mã {ma_chuc_vu} không tồn tại.")
        return self.repository.delete(ma_chuc_vu)
    
    def validPosition(self, position):
        if not position.ten_chuc_vu or not position.ten_chuc_vu.strip():
            raise ValueError("Tên chức vụ không được để trống.")
        if not position.ma_phong:
            raise ValueError("Mã phòng không được để trống.")
        return True