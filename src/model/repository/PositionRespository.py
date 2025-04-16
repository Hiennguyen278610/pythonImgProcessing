import mysql.connector
from src.model.entity.EmployeeEntity import Employee
from src.model.entity.PositionEntity import Position
from src.utils.databaseUtil import connectDatabase

class PositionRespository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        return mysql.connector.connect(**self.config)

    def findById(self, ma_chuc_vu):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM chuc_vu WHERE ma_chuc_vu = %s"""
        position = None

        try:
            cursor.execute(query, (ma_chuc_vu,))
            result = cursor.fetchone()

            if result:
                (ma_chuc_vu, ma_phong, ten_chuc_vu) = result
                position = Position(
                    ma_chuc_vu=ma_chuc_vu,
                    ma_phong=ma_phong,
                    ten_chuc_vu=ten_chuc_vu
                )
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()

        return position
    
    def findAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM chuc_vu"""
        positions = []

        try:
            cursor.execute(query)
            for (ma_chuc_vu, ma_phong, ten_chuc_vu) in cursor:
                position = Position(
                    ma_chuc_vu=ma_chuc_vu,
                    ma_phong=ma_phong,
                    ten_chuc_vu=ten_chuc_vu
                )
                positions.append(position)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

        return positions

    def findByDepartment(self, ma_phong):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM chuc_vu WHERE ma_phong = %s"""
        positions = []

        try:
            cursor.execute(query, (ma_phong,))
            for (ma_chuc_vu, ma_phong, ten_chuc_vu) in cursor:
                position = Position(
                    ma_chuc_vu=ma_chuc_vu,
                    ma_phong=ma_phong,
                    ten_chuc_vu=ten_chuc_vu
                )
                positions.append(position)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

        return positions

    def save(self, position):
        connection = self.getConnection()
        cursor = connection.cursor()

        query = """INSERT INTO chuc_vu (ma_chuc_vu, ma_phong, ten_chuc_vu) VALUES (%s, %s, %s)
                  ON DUPLICATE KEY UPDATE ma_phong = %s, ten_chuc_vu = %s"""
        
        data = (
            position.ma_chuc_vu,
            position.ma_phong,
            position.ten_chuc_vu,
            position.ma_phong,
            position.ten_chuc_vu
        )
        
        try:
            cursor.execute(query, data)
            connection.commit()
            return position
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    def delete(self, ma_chuc_vu):
        connection = self.getConnection()
        cursor = connection.cursor()
        
        query = "DELETE FROM chuc_vu WHERE ma_chuc_vu = %s"
        
        try:
            cursor.execute(query, (ma_chuc_vu,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()