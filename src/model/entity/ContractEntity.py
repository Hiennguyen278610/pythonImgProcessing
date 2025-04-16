from datetime import datetime

class Contract:
    def __init__(self, ma_hop_dong: int, ma_nhan_vien: int, thoi_han: str = None, 
                 ngay_ky: datetime = None, muc_luong: float = None):
        self.ma_hop_dong = ma_hop_dong
        self.ma_nhan_vien = ma_nhan_vien
        self.thoi_han = thoi_han
        self.ngay_ky = ngay_ky
        self.muc_luong = muc_luong
    
    def __str__(self):
        ngay_ky_str = self.ngay_ky.strftime('%Y-%m-%d') if self.ngay_ky else "N/A"
        return f"Contract [ID={self.ma_hop_dong}, EmployeeID={self.ma_nhan_vien}, Term={self.thoi_han}, SigningDate={ngay_ky_str}, Salary={self.muc_luong}]"