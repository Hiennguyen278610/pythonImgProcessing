from src.service.DepartmentService import DepartmentService
from src.service.PositionService import PositionService


from src.service.PositionService import PositionService


class PositionController:

    def __init__(self):
        self.positionService = PositionService()
        self.departmentService = DepartmentService()
        self.service = PositionService()

    def getAll(self):
        return self.service.getAll()

    def search(self, keyword):
        return self.service.search(keyword)

    def add(self, ma_phong, ten_chuc_vu):
        try:
            if isinstance(ma_phong, str):
                ma_phong = int(ma_phong)

            position_data = {
                'ma_phong': ma_phong,
                'ten_chuc_vu': ten_chuc_vu
            }


            result = self.service.createPosition(position_data)
            return True, "Thêm chức vụ thành công."
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Lỗi khi thêm chức vụ: {str(e)}"

    def update(self, ma_chuc_vu, ma_phong, ten_chuc_vu):

        try:
            if isinstance(ma_chuc_vu, str):
                ma_chuc_vu = int(ma_chuc_vu)
            if isinstance(ma_phong, str):
                ma_phong = int(ma_phong)

            position_data = {
                'ma_phong': ma_phong,
                'ten_chuc_vu': ten_chuc_vu
            }

            result = self.service.updatePosition(ma_chuc_vu, position_data)
            return True, "Cập nhật chức vụ thành công."
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Lỗi khi cập nhật chức vụ: {str(e)}"

    def getChucVu(self, ma_chuc_vu):
        position = self.positionService.getPositionByID(ma_chuc_vu)
        if position is None:
            return ""
        else: return position.ten_chuc_vu
    def delete(self, ma_chuc_vu):
        try:
            if isinstance(ma_chuc_vu, str):
                ma_chuc_vu = int(ma_chuc_vu)


    def getPhong(self, ma_chuc_vu):
        position = self.positionService.getPositionByID(ma_chuc_vu)
        department = self.departmentService.getDepartmentByID(position.ma_phong)
        if position is None:
            return ""
        else: return department.ten_phong
            result = self.service.deletePosition(ma_chuc_vu)
            return True, "Xóa chức vụ thành công."
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Lỗi khi xóa chức vụ: {str(e)}"

    def getById(self, ma_chuc_vu):
        try:
            if isinstance(ma_chuc_vu, str):
                ma_chuc_vu = int(ma_chuc_vu)

            return self.service.getPositionByID(ma_chuc_vu)
        except Exception:
            return None