import mysql.connector
from src.model.entity.EmployeeEntity import Employee
from src.utils.databaseUtil import connectDatabase

class PositionRespository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        return mysql.connector.connect(**self.config)