import mysql.connector
from CTkMessagebox import CTkMessagebox
from src.utils.databaseUtil import connectDatabase
from src.model.entity.loginEntity import LoginEntity

class LoginRepository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            return None

    def check_login(self, username, password, loginPanel):
        try:
            c = self.getConnection()
            if not c:
                return False, None  # Return early if connection failed

            cursor = c.cursor()
            query = """
                SELECT tk.ma_nhan_vien, tk.username, tk.password, nv.ho_ten_nhan_vien
                FROM tai_khoan tk
                         JOIN nhan_vien nv ON tk.ma_nhan_vien = nv.ma_nhan_vien
                         JOIN chuc_vu cv ON nv.ma_chuc_vu = cv.ma_chuc_vu
                WHERE tk.username = %s 
                  AND tk.password = %s
                  AND cv.ma_chuc_vu = 1
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                loginE = LoginEntity(ma_nhan_vien=result[0], username=result[1], password=result[2], ho_ten_nhan_vien=result[3])
                return True, loginE
            else:
                return False, None
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return False, None
        finally:
            if cursor:
                cursor.close()
            if c:
                c.close()
