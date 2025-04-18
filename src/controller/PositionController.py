# File: src/controller/PositionController.py
from src.service.PositionService import PositionService

class PositionController:
    def __init__(self):
        self.service = PositionService()

    def getAll(self):
        return self.service.getAll()

    def search(self, field, keyword):
        return self.service.search(field, keyword)

    def add(self, ma_chuc_vu, ma_phong, ten_chuc_vu):
        try:
            self.service.createPosition({
                'ma_chuc_vu': ma_chuc_vu,
                'ma_phong': ma_phong,
                'ten_chuc_vu': ten_chuc_vu
            })
            return True, "Thêm chức vụ thành công"
        except Exception as e:
            return False, str(e)


    def update(self, ma_chuc_vu, ma_phong, ten_chuc_vu):
        try:

            update_data = {
                'ma_phong': ma_phong,
                'ten_chuc_vu': ten_chuc_vu
            }
            self.service.updatePosition(ma_chuc_vu, update_data)
            return True, "Cập nhật chức vụ thành công"
        except Exception as e:
            return False, str(e)

    def delete(self, ma_chuc_vu):
        try:
            ok = self.service.deletePosition(ma_chuc_vu)
            if ok:
                return True, "Xóa chức vụ thành công"
            else:
                return False, "Không tìm thấy chức vụ để xóa"
        except Exception as e:
            return False, str(e)
