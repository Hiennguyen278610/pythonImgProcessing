import mysql.connector
from src.model.entity.DepartmentEntity import Department
from src.utils.databaseUtil import connectDatabase

class DepartmentRespository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        return mysql.connector.connect(**self.config)
    
    def findAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM phong"""
        departments = []
        
        try:
            cursor.execute(query)
            for (ma_phong, ma_truong_phong, ten_phong) in cursor:
                department = Department(
                    ma_phong=ma_phong,
                    ma_truong_phong=ma_truong_phong,
                    ten_phong=ten_phong
                )
                departments.append(department)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
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