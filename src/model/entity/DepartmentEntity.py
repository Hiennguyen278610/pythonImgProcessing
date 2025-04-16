class Department:
    def __init__(self, ma_phong: int, ma_truong_phong: int = None, ten_phong: str = None):
        self.ma_phong = ma_phong
        self.ma_truong_phong = ma_truong_phong
        self.ten_phong = ten_phong
    
    def __str__(self):
        return f"Department [ID={self.ma_phong}, Name={self.ten_phong}]"