import mysql.connector
from src.model.entity.AttendanceEntity import Attendance
from src.utils.databaseUtil import connectDatabase
from datetime import datetime, date

class AttendanceRepository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        return mysql.connector.connect(**self.config)

    def findAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM cham_cong"""
        attendances = []
        
        try:
            cursor.execute(query)
            for (ma_nhan_vien, ngay_cham_cong, gio_vao, gio_ra, img) in cursor:
                attendance = Attendance(
                    ma_nhan_vien=ma_nhan_vien,
                    ngay_cham_cong=ngay_cham_cong,
                    gio_vao=gio_vao,
                    gio_ra=gio_ra,
                    img=img
                )
                attendances.append(attendance)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()
            
        return attendances

    def findByEmployeeIdAndDate(self, ma_nhan_vien, ngay_cham_cong):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM cham_cong WHERE ma_nhan_vien = %s AND ngay_cham_cong = %s"""
        attendance = None
        
        try:
            cursor.execute(query, (ma_nhan_vien, ngay_cham_cong))
            result = cursor.fetchone()
            
            if result:
                (ma_nhan_vien, ngay_cham_cong, gio_vao, gio_ra, img) = result
                attendance = Attendance(
                    ma_nhan_vien=ma_nhan_vien,
                    ngay_cham_cong=ngay_cham_cong,
                    gio_vao=gio_vao,
                    gio_ra=gio_ra,
                    img=img
                )
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()
            
        return attendance

    def findByEmployeeId(self, ma_nhan_vien):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM cham_cong WHERE ma_nhan_vien = %s"""
        attendances = []
        
        try:
            cursor.execute(query, (ma_nhan_vien,))
            for (ma_nhan_vien, ngay_cham_cong, gio_vao, gio_ra, img_checkin, img_checkout) in cursor:
                attendance = Attendance(
                    ma_nhan_vien=ma_nhan_vien,
                    ngay_cham_cong=ngay_cham_cong,
                    gio_vao=gio_vao,
                    gio_ra=gio_ra,
                    img_checkin = img_checkin,
                    img_checkout = img_checkout
                )
                attendances.append(attendance)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()
            
        return attendances

    def findByDate(self, ngay_cham_cong):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM cham_cong WHERE ngay_cham_cong = %s"""
        attendances = []
        
        try:
            cursor.execute(query, (ngay_cham_cong,))
            for (ma_nhan_vien, ngay_cham_cong, gio_vao, gio_ra, img) in cursor:
                attendance = Attendance(
                    ma_nhan_vien=ma_nhan_vien,
                    ngay_cham_cong=ngay_cham_cong,
                    gio_vao=gio_vao,
                    gio_ra=gio_ra,
                    img=img
                )
                attendances.append(attendance)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()
            
        return attendances

    def save(self, attendance):
        connection = self.getConnection()
        cursor = connection.cursor()
        
        # Since this table has composite primary key, we use REPLACE
        query = """REPLACE INTO cham_cong 
                (ma_nhan_vien, ngay_cham_cong, gio_vao, gio_ra, img) 
                VALUES (%s, %s, %s, %s, %s)"""
        
        data = (
            attendance.ma_nhan_vien,
            attendance.ngay_cham_cong,
            attendance.gio_vao,
            attendance.gio_ra,
            attendance.img
        )
        
        try:
            cursor.execute(query, data)
            connection.commit()
            return attendance
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    def delete(self, ma_nhan_vien, ngay_cham_cong):
        connection = self.getConnection()
        cursor = connection.cursor()
        
        query = "DELETE FROM cham_cong WHERE ma_nhan_vien = %s AND ngay_cham_cong = %s"
        
        try:
            cursor.execute(query, (ma_nhan_vien, ngay_cham_cong))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

    def getTodayRecord(self, ma_nhan_vien):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM cham_cong WHERE ma_nhan_vien = %s AND ngay_cham_cong = CURDATE()"""
        cursor.execute(query, (ma_nhan_vien,))
        return cursor.fetchone()

    def insertCheckin(self, ma_nhan_vien, urlImg):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """INSERT INTO cham_cong (ma_nhan_vien, ngay_cham_cong, gio_vao, img_checkin) VALUES (%s, CURDATE(), NOW(), %s)"""
        cursor.execute(query, (ma_nhan_vien, urlImg,))
        connection.commit()

    def updateCheckout(self, ma_nhan_vien, urlImg):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """UPDATE cham_cong SET gio_ra = NOW(), img_checkout = %s WHERE ma_nhan_vien = %s AND ngay_cham_cong = CURDATE()"""
        cursor.execute(query, (urlImg, ma_nhan_vien))
        connection.commit()


    def getAttendanceYearById(self, ma_nhan_vien):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT distinct YEAR(ngay_cham_cong) FROM cham_cong WHERE ma_nhan_vien = %s"""
        years = []

        try:
            cursor.execute(query, (ma_nhan_vien,))
            years = [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

        return years
