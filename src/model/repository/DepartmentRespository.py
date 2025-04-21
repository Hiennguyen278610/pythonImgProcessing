import mysql.connector
from src.model.entity.DepartmentEntity import Department
from src.utils.databaseUtil import connectDatabase


class DepartmentRespository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            return None

    def findAll(self):
        connection = self.getConnection()
        if not connection:
            return []
        cursor = connection.cursor()
        query = "SELECT ma_phong, ma_truong_phong, ten_phong FROM phong"
        departments = []
        try:
            cursor.execute(query)
            for (ma_phong, ma_truong_phong, ten_phong) in cursor:
                departments.append(Department(ma_phong=ma_phong, ma_truong_phong=ma_truong_phong, ten_phong=ten_phong))

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()
        return departments

    def findById(self, ma_phong):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM phong WHERE ma_phong = %s"""
        department = None

        try:
            cursor.execute(query, (ma_phong,))
            result = cursor.fetchone()

            if result:
                (ma_phong, ma_truong_phong, ten_phong) = result
                department = Department(
                    ma_phong=ma_phong,
                    ma_truong_phong=ma_truong_phong,
                    ten_phong=ten_phong
                )
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()

        return department

    def save(self, department):
        connection = self.getConnection()
        cursor = connection.cursor()

        if department.ma_phong is None:
            query = """INSERT INTO phong (ma_truong_phong, ten_phong) VALUES (%s, %s)"""

            data = (
                department.ma_truong_phong,
                department.ten_phong
            )

            try:
                cursor.execute(query, data)
                connection.commit()
                department.ma_phong = cursor.lastrowid
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
            finally:
                cursor.close()
                connection.close()
        else:
            query = """UPDATE phong
                    SET ma_truong_phong = %s, ten_phong = %s
                    WHERE ma_phong = %s"""

            data = (
                department.ma_truong_phong,
                department.ten_phong,
                department.ma_phong
            )

            try:
                cursor.execute(query, data)
                connection.commit()
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
            finally:
                cursor.close()
                connection.close()

        return department

    def delete(self, ma_phong):
        connection = self.getConnection()
        cursor = connection.cursor()

        query = "DELETE FROM phong WHERE ma_phong = %s"

        try:
            cursor.execute(query, (ma_phong,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

    def search(self, search_text, keyword):
        valid_fields = ['ma_phong', 'ma_truong_phong', 'ten_phong']
        if search_text not in valid_fields:
            return []

        connection = self.getConnection()
        if not connection:
            return []

        cursor = connection.cursor()
        query = f"SELECT * FROM phong WHERE {search_text} LIKE %s"

        try:
            cursor.execute(query, (f"%{keyword}%",))
            departments = [Department(*row) for row in cursor]
            return departments
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

