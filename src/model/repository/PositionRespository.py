import mysql.connector
from src.model.entity.PositionEntity import Position
from src.utils.databaseUtil import connectDatabase


class PositionRespository:
    def __init__(self, config=None):
        self.config = connectDatabase() if config is None else config

    def getConnection(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            return None

    def search(self, field, keyword):
        allowed = {'ma_chuc_vu', 'ten_chuc_vu', 'ma_phong'}
        if field not in allowed:
            return []
        conn = self.getConnection()
        if not conn:
            return []
        cur = conn.cursor()
        sql = f"SELECT * FROM chuc_vu WHERE {field} LIKE %s"
        cur.execute(sql, (f"%{keyword}%",))
        rows = [Position(*row) for row in cur]
        cur.close()
        conn.close()
        return rows

    def findById(self, ma_chuc_vu):
        connection = self.getConnection()
        if not connection:
            return None
        cursor = connection.cursor()
        query = """SELECT * FROM chuc_vu WHERE ma_chuc_vu = %s"""
        position = None
        try:
            cursor.execute(query, (ma_chuc_vu,))
            result = cursor.fetchone()
            if result:
                (ma_chuc_vu, ma_phong, ten_chuc_vu) = result
                position = Position(ma_chuc_vu, ma_phong, ten_chuc_vu)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()
        return position

    def findAll(self):
        connection = self.getConnection()
        if not connection:
            return []
        cursor = connection.cursor()
        query = "SELECT * FROM chuc_vu"
        positions = []
        try:
            cursor.execute(query)
            for (ma_chuc_vu, ma_phong, ten_chuc_vu) in cursor:
                positions.append(Position(ma_chuc_vu, ma_phong, ten_chuc_vu))
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()
        return positions

    def findByDepartment(self, ma_phong):
        connection = self.getConnection()
        if not connection:
            return []
        cursor = connection.cursor()
        query = "SELECT * FROM chuc_vu WHERE ma_phong = %s"
        positions = []
        try:
            cursor.execute(query, (ma_phong,))
            for (ma_chuc_vu, ma_phong, ten_chuc_vu) in cursor:
                positions.append(Position(ma_chuc_vu, ma_phong, ten_chuc_vu))
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            connection.close()
        return positions



    def insert(self, position):
        connection = self.getConnection()
        if not connection:
            return None
        cursor = connection.cursor()

        check_query = "SELECT COUNT(*) FROM chuc_vu WHERE ma_chuc_vu = %s"
        cursor.execute(check_query, (position.ma_chuc_vu,))
        if cursor.fetchone()[0] > 0:
            cursor.close()
            connection.close()
            raise ValueError(f"Mã chức vụ {position.ma_chuc_vu} đã tồn tại.")

        query = """INSERT INTO chuc_vu (ma_chuc_vu, ma_phong, ten_chuc_vu) VALUES (%s, %s, %s)"""
        data = (position.ma_chuc_vu, position.ma_phong, position.ten_chuc_vu)
        try:
            cursor.execute(query, data)
            connection.commit()
            return position
        except mysql.connector.Error as err:
            if err.errno == 1452:  # 1452	Lỗi khóa ngoại không hợp lệ(1062	Lỗi khóa chính trùng (Duplicate entry), 1451	Không thể xóa vì còn ràng buộc khóa ngoại)
                raise ValueError(f"Mã phòng {position.ma_phong} không tồn tại trong hệ thống.")
            print(f"Database error: {err}")
            raise err
        finally:
            cursor.close()
            connection.close()

    def update(self, position):
        connection = self.getConnection()
        if not connection:
            return None
        cursor = connection.cursor()
        query = """UPDATE chuc_vu SET ma_phong = %s, ten_chuc_vu = %s WHERE ma_chuc_vu = %s"""
        data = (position.ma_phong, position.ten_chuc_vu, position.ma_chuc_vu)
        try:
            cursor.execute(query, data)
            connection.commit()
            return position
        except mysql.connector.Error as err:
            if err.errno == 1452:
                raise ValueError(f"Mã phòng {position.ma_phong} không tồn tại trong hệ thống.")
            print(f"Database error: {err}")
            raise err
        finally:
            cursor.close()
            connection.close()

    def delete(self, ma_chuc_vu):
        connection = self.getConnection()
        if not connection:
            return False
        cursor = connection.cursor()

        # Check for dependencies (e.g., in employees table)
        # dependency_query = "SELECT COUNT(*) FROM nhan_vien join phan_cong on nhan_vien.ma_nhan_vien = phan_cong.ma_nhan_vien WHERE ma_chuc_vu = %s"
        query_phan_cong = "DELETE FROM phan_cong WHERE ma_chuc_vu = %s"
        try:
            cursor.execute(query_phan_cong, (ma_chuc_vu,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Database error 1 : {err}")
        try:
            # cursor.execute(dependency_query, (ma_chuc_vu,))
            query = "DELETE FROM chuc_vu WHERE ma_chuc_vu = %s"
            cursor.execute(query, (ma_chuc_vu,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Database error 2: {err}")
            raise err
        finally:
            cursor.close()
            connection.close()

    def deleteByDepartmentId(self, ma_phong):
        connection = self.getConnection()
        if not connection:
            return False
        cursor = connection.cursor()
        try:
            # Xóa các dòng trong phan_cong liên kết với chức vụ thuộc phòng này
            cursor.execute("""
                DELETE FROM phan_cong 
                WHERE ma_chuc_vu IN (SELECT ma_chuc_vu FROM chuc_vu WHERE ma_phong = %s)
            """, (ma_phong,))
            connection.commit()

            # Xóa chức vụ thuộc phòng này
            cursor.execute("DELETE FROM chuc_vu WHERE ma_phong = %s", (ma_phong,))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Database error in deleteByDepartmentId: {err}")
            raise err
        finally:
            cursor.close()
            connection.close()

    def checkDepartmentExists(self, ma_phong):
        connection = self.getConnection()
        if not connection:
            return False
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM phong WHERE ma_phong = %s"
        try:
            cursor.execute(query, (ma_phong,))
            count = cursor.fetchone()[0]
            return count > 0
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()