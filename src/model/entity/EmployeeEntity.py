from datetime import datetime

class Employee:
    def __init__(self, ma_nhan_vien: int, ma_ngql: int = None,
                 ma_chuc_vu: int = None, ho_ten_nhan_vien: str = None, 
                 ngay_sinh: datetime = None, so_dien_thoai: str = None, 
                 dia_chi: str = None, gioi_tinh: str = None, 
                 ngay_vao_lam: datetime = None, url_image: str = None):
        self.ma_nhan_vien = ma_nhan_vien
        self.ma_ngql = ma_ngql
        self.ma_chuc_vu = ma_chuc_vu
        self.ho_ten_nhan_vien = ho_ten_nhan_vien
        self.ngay_sinh = ngay_sinh
        self.so_dien_thoai = so_dien_thoai
        self.dia_chi = dia_chi
        self.gioi_tinh = gioi_tinh
        self.ngay_vao_lam = ngay_vao_lam
        self.url_image = url_image
    
    def __str__(self):
        return f"Employee [ID={self.ma_nhan_vien}, Name={self.ho_ten_nhan_vien}]"