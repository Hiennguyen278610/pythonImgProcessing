class Position:
    def __init__(self, ma_chuc_vu=None, ma_phong=None, ten_chuc_vu=None):
        self.ma_chuc_vu = ma_chuc_vu
        self.ma_phong = ma_phong
        self.ten_chuc_vu = ten_chuc_vu

    def __str__(self):
        return f"Position [ID={self.ma_chuc_vu}, Name={self.ten_chuc_vu}]"