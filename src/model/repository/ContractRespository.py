import mysql.connector
from src.model.entity.ContractEntity import Contract
from src.utils.databaseUtil import connectDatabase

class ContractRepository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        return mysql.connector.connect(**self.config)

    def findAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM Contract"""
        contracts = []
        
        try:
            cursor.execute(query)
            for (contractID, employeeID, term, signingDate, salary) in cursor:
                contract = Contract(
                    contractID=contractID,
                    employeeID=employeeID,
                    term=term,
                    signingDate=signingDate,
                    salary=salary
                )
                contracts.append(contract)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()
            
        return contracts

    def findByID(self, contractID):
        connection = self.getConnection()
        cursor = connection.cursor()  
        query = """SELECT * FROM Contract WHERE contractID = %s"""
        contract = None
        
        try:
            cursor.execute(query, (contractID,))
            result = cursor.fetchone()
            
            if result:
                (contractID, employeeID, term, signingDate, salary) = result
                contract = Contract(
                    contractID=contractID,
                    employeeID=employeeID,
                    term=term,
                    signingDate=signingDate,
                    salary=salary
                )
        finally:
            cursor.close()
            connection.close()
            
        return contract
        
    def findByEmployeeID(self, employeeID):
        connection = self.getConnection()
        cursor = connection.cursor()  
        query = """SELECT * FROM Contract WHERE employeeID = %s"""
        contracts = []
        
        try:
            cursor.execute(query, (employeeID,))
            for (contractID, employeeID, term, signingDate, salary) in cursor:
                contract = Contract(
                    contractID=contractID,
                    employeeID=employeeID,
                    term=term,
                    signingDate=signingDate,
                    salary=salary
                )
                contracts.append(contract)
        finally:
            cursor.close()
            connection.close()
            
        return contracts

    def save(self, contract):
        connection = self.getConnection()
        cursor = connection.cursor()
        
        if contract.contractID is None:
            query = """INSERT INTO Contract (employeeID, term, signingDate, salary) VALUES (%s, %s, %s, %s)"""
            
            data = (
                contract.employeeID, 
                contract.term, 
                contract.signingDate, 
                contract.salary
            )
            
            try:
                cursor.execute(query, data)
                connection.commit()
                contract.contractID = cursor.lastrowid
            finally:
                cursor.close()
                connection.close()
        else:
            query = """UPDATE Contract
                    SET employeeID = %s, term = %s, signingDate = %s, salary = %s
                    WHERE contractID = %s"""
            
            data = (
                contract.employeeID,
                contract.term,
                contract.signingDate,
                contract.salary,
                contract.contractID
            )
            
            try:
                cursor.execute(query, data)
                connection.commit()
            finally:
                cursor.close()
                connection.close()
                
        return contract

    def delete(self, contractID):
        connection = self.getConnection()
        cursor = connection.cursor()
        
        query = "DELETE FROM Contract WHERE contractID = %s"
        
        try:
            cursor.execute(query, (contractID,))
            connection.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            connection.close()