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
        query = """SELECT * FROM Employee"""
        employees = []

        try:
            cursor.execute(query)
            for (employeeID, managerID, roleID, name, dob,
                 phone, address, gender, startDate) in cursor:
                employee = Employee(
                    employeeID=employeeID,
                    managerID=managerID,
                    roleID=roleID,
                    name=name,
                    dob=dob,
                    phone=phone,
                    address=address,
                    gender=gender,
                    startDate=startDate
                )
                employees.append(employee)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

        return employees

    def findByID(self, employeeID):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM Employee WHERE employeeID = %s"""
        employee = None

        try:
            cursor.execute(query, (employeeID,))
            result = cursor.fetchone()

            if result:
                (employeeID, managerID, roleID, name, dob, phone, address, gender, startDate) = result
                employee = Employee(
                    employeeID=employeeID,
                    managerID=managerID,
                    roleID=roleID,
                    name=name,
                    dob=dob,
                    phone=phone,
                    address=address,
                    gender=gender,
                    startDate=startDate
                )
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()

        return employee

    def save(self, employee): # Gồm xử lí thêm và sửa
        connection = self.getConnection()
        cursor = connection.cursor()

        if employee.employeeID is None:
            query = """INSERT INTO Employee (managerID, roleID, name, dob, phone, address, gender, startDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

            data = (
                employee.managerID,
                employee.roleID,
                employee.name,
                employee.dob,
                employee.phone,
                employee.address,
                employee.gender,
                employee.startDate
            )

            try:
                cursor.execute(query, data)
                connection.commit()
                employee.employeeID = cursor.lastrowid #Tạo ID tự động
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
            finally:
                cursor.close()
                connection.close()
        else:
            query = """UPDATE Employee
            SET managerID = %s, roleID = %s, name = %s, dob = %s, phone = %s, address = %s, gender = %s, startDate = %s
            WHERE employeeID = %s"""

            data = (
                employee.managerID,
                employee.roleID,
                employee.name,
                employee.dob,
                employee.phone,
                employee.address,
                employee.gender,
                employee.startDate,
                employee.employeeID
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

    def delete(self, employeeID):
        connection = self.getConnection()
        cursor = connection.cursor()

        query = "DELETE FROM Employee WHERE employeeID = %s"

        try:
            cursor.execute(query, (employeeID,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

    def findByName(self, name):
        connection = self.getConnection()
        cursor = connection.cursor()

        query = """SELECT * FROM Employee WHERE name LIKE %s"""
        employees = []

        try:
            cursor.execute(query, (f"%{name}%",))
            for (employeeID, managerID, roleID, name, dob, phone, address, gender, startDate) in cursor:
                employee = Employee(
                    employeeID=employeeID,
                    managerID=managerID,
                    roleID=roleID,
                    name=name,
                    dob=dob,
                    phone=phone,
                    address=address,
                    gender=gender,
                    startDate=startDate
                )
                employees.append(employee)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

        return employees