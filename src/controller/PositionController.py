from src.service.DepartmentService import DepartmentService
from src.service.PositionService import PositionService


class PositionController:
    def __init__(self):
        self.positionService = PositionService()
        self.departmentService = DepartmentService()

    def getChucVu(self, ma_chuc_vu):
        position = self.positionService.getPositionByID(ma_chuc_vu)
        if position is None:
            return ""
        else: return position.ten_chuc_vu


    def getPhong(self, ma_chuc_vu):
        position = self.positionService.getPositionByID(ma_chuc_vu)
        department = self.departmentService.getDepartmentByID(position.ma_phong)
        if position is None:
            return ""
        else: return department.ten_phong