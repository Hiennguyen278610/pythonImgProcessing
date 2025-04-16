import mysql.connector
from src.model.entity.EmployeeEntity import Employee
from src.utils.databaseUtil import connectDatabase

class EmployeeRepository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        return mysql.connector.connect(**self.config)

    def findAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM nhan_vien"""
        employees = []

        try:
            cursor.execute(query)
            for (ma_nhan_vien, ma_ngql, ma_chuc_vu, ho_ten_nhan_vien,
                ngay_sinh, so_dien_thoai, dia_chi, gioi_tinh, ngay_vao_lam, url_image) in cursor:
                employee = Employee(
                    ma_nhan_vien=ma_nhan_vien,
                    ma_ngql=ma_ngql,
                    ma_chuc_vu=ma_chuc_vu,
                    ho_ten_nhan_vien=ho_ten_nhan_vien,
                    ngay_sinh=ngay_sinh,
                    so_dien_thoai=so_dien_thoai,
                    dia_chi=dia_chi,
                    gioi_tinh=gioi_tinh,
                    ngay_vao_lam=ngay_vao_lam,
                    url_image=url_image
                )
                employees.append(employee)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

        return employees

    def findByID(self, ma_nhan_vien):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM nhan_vien WHERE ma_nhan_vien = %s"""
        employee = None

        try:
            cursor.execute(query, int(ma_nhan_vien,))
            result = cursor.fetchone()

            if result:
                (ma_nhan_vien, ma_phong, ma_ngql, ma_chuc_vu, ho_ten_nhan_vien, 
                ngay_sinh, so_dien_thoai, dia_chi, gioi_tinh, ngay_vao_lam, url_image) = result
                employee = Employee(
                    ma_nhan_vien=ma_nhan_vien,
                    ma_phong=ma_phong,
                    ma_ngql=ma_ngql,
                    ma_chuc_vu=ma_chuc_vu,
                    ho_ten_nhan_vien=ho_ten_nhan_vien,
                    ngay_sinh=ngay_sinh,
                    so_dien_thoai=so_dien_thoai,
                    dia_chi=dia_chi,
                    gioi_tinh=gioi_tinh,
                    ngay_vao_lam=ngay_vao_lam,
                    url_image=url_image
                )
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()

        return employee

    def save(self, employee):
        connection = self.getConnection()
        cursor = connection.cursor()

        if employee.ma_nhan_vien is None:
            query = """INSERT INTO nhan_vien (ma_phong, ma_ngql, ma_chuc_vu, ho_ten_nhan_vien, 
                    ngay_sinh, so_dien_thoai, dia_chi, gioi_tinh, ngay_vao_lam, url_image) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            data = (
                employee.ma_phong,
                employee.ma_ngql,
                employee.ma_chuc_vu,
                employee.ho_ten_nhan_vien,
                employee.ngay_sinh,
                employee.so_dien_thoai,
                employee.dia_chi,
                employee.gioi_tinh,
                employee.ngay_vao_lam,
                employee.url_image
            )

            try:
                cursor.execute(query, data)
                connection.commit()
                employee.ma_nhan_vien = cursor.lastrowid
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
            finally:
                cursor.close()
                connection.close()
        else:
            query = """UPDATE nhan_vien
                    SET ma_phong = %s, ma_ngql = %s, ma_chuc_vu = %s, ho_ten_nhan_vien = %s,
                    ngay_sinh = %s, so_dien_thoai = %s, dia_chi = %s, gioi_tinh = %s, 
                    ngay_vao_lam = %s, url_image = %s
                    WHERE ma_nhan_vien = %s"""

            data = (
                employee.ma_phong,
                employee.ma_ngql,
                employee.ma_chuc_vu,
                employee.ho_ten_nhan_vien,
                employee.ngay_sinh,
                employee.so_dien_thoai,
                employee.dia_chi,
                employee.gioi_tinh,
                employee.ngay_vao_lam,
                employee.url_image,
                employee.ma_nhan_vien
            )

            try:
                cursor.execute(query, data)
                connection.commit()
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
            finally:
                cursor.close()
                connection.close()

        return employee

    def delete(self, ma_nhan_vien):
        connection = self.getConnection()
        cursor = connection.cursor()

        query = "DELETE FROM nhan_vien WHERE ma_nhan_vien = %s"

        try:
            cursor.execute(query, (ma_nhan_vien,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

    def findByName(self, ho_ten_nhan_vien):
        connection = self.getConnection()
        cursor = connection.cursor()

        query = """SELECT * FROM nhan_vien WHERE ho_ten_nhan_vien LIKE %s"""
        employees = []

        try:
            cursor.execute(query, (f"%{ho_ten_nhan_vien}%",))
            for (ma_nhan_vien, ma_phong, ma_ngql, ma_chuc_vu, ho_ten_nhan_vien, 
                ngay_sinh, so_dien_thoai, dia_chi, gioi_tinh, ngay_vao_lam, url_image) in cursor:
                employee = Employee(
                    ma_nhan_vien=ma_nhan_vien,
                    ma_phong=ma_phong,
                    ma_ngql=ma_ngql,
                    ma_chuc_vu=ma_chuc_vu,
                    ho_ten_nhan_vien=ho_ten_nhan_vien,
                    ngay_sinh=ngay_sinh,
                    so_dien_thoai=so_dien_thoai,
                    dia_chi=dia_chi,
                    gioi_tinh=gioi_tinh,
                    ngay_vao_lam=ngay_vao_lam,
                    url_image=url_image
                )
                employees.append(employee)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

        return employees