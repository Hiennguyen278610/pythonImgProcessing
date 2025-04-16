import mysql.connector
from src.model.entity.ContractEntity import Contract
from src.utils.databaseUtil import connectDatabase
from datetime import datetime

class ContractRepository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        return mysql.connector.connect(**self.config)

    def findAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        query = """SELECT * FROM hop_dong"""
        contracts = []
        
        try:
            cursor.execute(query)
            for (ma_hop_dong, ma_nhan_vien, thoi_han, ngay_ky, muc_luong) in cursor:
                contract = Contract(
                    ma_hop_dong=ma_hop_dong,
                    ma_nhan_vien=ma_nhan_vien,
                    thoi_han=thoi_han,
                    ngay_ky=ngay_ky,
                    muc_luong=muc_luong
                )
                contracts.append(contract)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()
            
        return contracts

    def findByID(self, ma_hop_dong):
        connection = self.getConnection()
        cursor = connection.cursor()  
        query = """SELECT * FROM hop_dong WHERE ma_hop_dong = %s"""
        contract = None
        
        try:
            cursor.execute(query, (ma_hop_dong,))
            result = cursor.fetchone()
            
            if result:
                (ma_hop_dong, ma_nhan_vien, thoi_han, ngay_ky, muc_luong) = result
                contract = Contract(
                    ma_hop_dong=ma_hop_dong,
                    ma_nhan_vien=ma_nhan_vien,
                    thoi_han=thoi_han,
                    ngay_ky=ngay_ky,
                    muc_luong=muc_luong
                )
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()
            
        return contract
        
    def findByEmployeeID(self, ma_nhan_vien):
        connection = self.getConnection()
        cursor = connection.cursor()  
        query = """SELECT * FROM hop_dong WHERE ma_nhan_vien = %s"""
        contracts = []
        
        try:
            cursor.execute(query, (ma_nhan_vien,))
            for (ma_hop_dong, ma_nhan_vien, thoi_han, ngay_ky, muc_luong) in cursor:
                contract = Contract(
                    ma_hop_dong=ma_hop_dong,
                    ma_nhan_vien=ma_nhan_vien,
                    thoi_han=thoi_han,
                    ngay_ky=ngay_ky,
                    muc_luong=muc_luong
                )
                contracts.append(contract)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()
            
        return contracts

    def save(self, contract):
        connection = self.getConnection()
        cursor = connection.cursor()
        
        if contract.ma_hop_dong is None:
            query = """INSERT INTO hop_dong (ma_nhan_vien, thoi_han, ngay_ky, muc_luong) VALUES (%s, %s, %s, %s)"""
            
            data = (
                contract.ma_nhan_vien, 
                contract.thoi_han, 
                contract.ngay_ky, 
                contract.muc_luong
            )
            
            try:
                cursor.execute(query, data)
                connection.commit()
                contract.ma_hop_dong = cursor.lastrowid
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
            finally:
                cursor.close()
                connection.close()
        else:
            query = """UPDATE hop_dong
                    SET ma_nhan_vien = %s, thoi_han = %s, ngay_ky = %s, muc_luong = %s
                    WHERE ma_hop_dong = %s"""
            
            data = (
                contract.ma_nhan_vien,
                contract.thoi_han,
                contract.ngay_ky,
                contract.muc_luong,
                contract.ma_hop_dong
            )
            
            try:
                cursor.execute(query, data)
                connection.commit()
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
            finally:
                cursor.close()
                connection.close()
                
        return contract

    def delete(self, ma_hop_dong):
        connection = self.getConnection()
        cursor = connection.cursor()
        
        query = "DELETE FROM hop_dong WHERE ma_hop_dong = %s"
        
        try:
            cursor.execute(query, (ma_hop_dong,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()