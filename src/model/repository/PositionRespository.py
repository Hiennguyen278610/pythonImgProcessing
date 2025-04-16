import mysql.connector
from src.model.entity.EmployeeEntity import Employee
from src.model.entity.PositionEntity import Position
from src.utils.databaseUtil import connectDatabase

class PositionRespository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        return mysql.connector.connect(**self.config)

    def findById(self, id):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM chuc_vu WHERE ma_chuc_vu = %s"""
        position = None

        try:
            cursor.execute(query, (id,))
            result = cursor.fetchone()

            if result:
                (ma_chuc_vu, ten_chuc_vu, ma_phong) = result
                position = Position(
                    ma_chuc_vu=ma_chuc_vu,
                    ten_chuc_vu=ten_chuc_vu,
                    ma_phong=ma_phong
                )
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()

        return position
