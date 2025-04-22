from datetime import datetime, time

class Attendance:
    def __init__(self, ma_nhan_vien: int, ngay_cham_cong: datetime, 
                 gio_vao: time = None, gio_ra: time = None, img_checkin: str = None, img_checkout: str = None):
        self.ma_nhan_vien = ma_nhan_vien
        self.ngay_cham_cong = ngay_cham_cong
        self.gio_vao = gio_vao
        self.gio_ra = gio_ra
        self.img_checkin = img_checkin
        self.img_checkout = img_checkout
    
    def __str__(self):
        ngay_str = self.ngay_cham_cong.strftime('%Y-%m-%d') if self.ngay_cham_cong else "N/A"
        return f"Attendance [EmployeeID={self.ma_nhan_vien}, Date={ngay_str}]"