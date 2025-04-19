from src.model.entity.PositionEntity import Position
from src.model.repository.PositionRespository import PositionRespository

class PositionService:

    def __init__(self):
        self.repository = PositionRespository()

    def getAll(self):
        return self.repository.findAll()

    def search(self, field, keyword):
        return self.repository.search(field, keyword)

    def getPositionByID(self, ma_chuc_vu):
        return self.repository.findById(ma_chuc_vu)

    def getPositionsByDepartment(self, ma_phong):
        return self.repository.findByDepartment(ma_phong)

    def createPosition(self, positionData):
        # Tạo entity có mã người dùng nhập
        position = Position(
            ma_chuc_vu=positionData.get('ma_chuc_vu'),
            ma_phong=positionData.get('ma_phong'),
            ten_chuc_vu=positionData.get('ten_chuc_vu')
        )

        self.validPosition(position)

        return self.repository.insert(position)

    def updatePosition(self, ma_chuc_vu, positionData):
        existPosition = self.repository.findById(ma_chuc_vu)
        if not existPosition:
            raise ValueError(f"Chức vụ có mã {ma_chuc_vu} không tồn tại.")

        # Cập nhật lại giá trị
        if 'ma_phong' in positionData:
            existPosition.ma_phong = positionData.get('ma_phong')
        if 'ten_chuc_vu' in positionData:
            existPosition.ten_chuc_vu = positionData.get('ten_chuc_vu')

        self.validPosition(existPosition)

        return self.repository.update(existPosition)

    def deletePosition(self, ma_chuc_vu):
        existPosition = self.repository.findById(ma_chuc_vu)
        if not existPosition:
            raise ValueError(f"Chức vụ có mã {ma_chuc_vu} không tồn tại.")
        return self.repository.delete(ma_chuc_vu)

    def validPosition(self, position):
        # Convert ma_chuc_vu to string for validation
        ma_chuc_vu_str = str(position.ma_chuc_vu) if position.ma_chuc_vu is not None else ""
        if not ma_chuc_vu_str.strip():
            raise ValueError("Mã chức vụ không được để trống.")
        if len(ma_chuc_vu_str.strip()) > 10:
            raise ValueError("Mã chức vụ không được vượt quá 10 ký tự.")

        if not position.ten_chuc_vu or not position.ten_chuc_vu.strip():
            raise ValueError("Tên chức vụ không được để trống.")

        if len(position.ten_chuc_vu.strip()) > 50:
            raise ValueError("Tên chức vụ không được vượt quá 50 ký tự.")

        if position.ma_phong is None:
            raise ValueError("Mã phòng không được để trống.")

        return True