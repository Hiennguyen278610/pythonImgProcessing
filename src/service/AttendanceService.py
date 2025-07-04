import face_recognition
import cv2
import os
import pickle
import numpy
from datetime import datetime
from src.model.repository.AttendanceRespository import AttendanceRepository
from src.model.repository.EmployeeRespository import EmployeeRepository

class AttendanceService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()
        self.employee_repo = EmployeeRepository()
        self.known_face_encodings = []
        self.known_face_id = []

    def load_known_faces(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
        face_img_dir = os.path.join(root_dir, "Resources", "faceImg")

        employees = self.employee_repo.findAll()
        for employee in employees:
            img_path = os.path.join(face_img_dir, employee.url_image)

            if not os.path.exists(img_path):
                print(f"[LỖI] Ảnh không tồn tại: {img_path}")
                continue

            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                self.known_face_encodings.append(encoding[0])
                self.known_face_id.append(employee.ma_nhan_vien)

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
        encode_path = os.path.join(project_root, "Resources", "EncodeFile.p")

        if not os.path.exists(encode_path):
            raise FileNotFoundError(f"Không tìm thấy file: {encode_path}")

        # Đọc file encoding
        with open(encode_path, 'rb') as f:
            data = pickle.load(f)
            self.known_face_encodings, self.known_face_id = data

    def load_file_encode(self):
        try:
            with open("src/../Resources/EncodeFile.p", 'rb') as file:
                encodeWithId = pickle.load(file)
                self.known_face_encodings, self.known_face_id = encodeWithId
                print(len(self.known_face_encodings))
        except:
            self.known_face_encodings, self.known_face_id = [], []
            print(len(self.known_face_encodings))

    def add_new_face(self, new_employee):
        try:
            with open("../../Resources/EncodeFile.p", 'rb') as file:
                encodeWithId = pickle.load(file)
                known_encodings, known_ids = encodeWithId
        except:
            known_encodings, known_ids = [], []
        path = os.path.join("..\\..\\..\\Resources", new_employee.urlImage)
        path = os.path.normpath(path)
        if not os.path.exists(path):
            return
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            return
        known_encodings.append(encodings[0])
        known_ids.append(new_employee.id)
        with open("../../Encodings/EncodeFile.p", 'wb') as file:
            pickle.dump([known_encodings, known_ids], file)

    def locationFace(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return face_recognition.face_locations(rgb_frame)

    def recognize_and_mark_attendance(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        id = -1
        if face_locations and face_encodings and self.known_face_encodings:
            encode_face = face_encodings[0]
            matches = face_recognition.compare_faces(self.known_face_encodings, encode_face)
            face_distances = face_recognition.face_distance(self.known_face_encodings, encode_face)
            if len(face_distances) > 0:
                match_index = numpy.argmin(face_distances)
                if matches[match_index] and face_distances[match_index] < 0.45:
                    id = match_index + 1

        return id

    def get_employee_attendance(self, frame):
        id = self.recognize_and_mark_attendance(frame)
        print(id)
        if id == -1: return None
        employee_attendance = self.employee_repo.findByID(id)
        return employee_attendance

    def save_attendance_img(self, frame, ma_nhan_vien):
        today = datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H-%M-%S")
        folder_path = os.path.join("scr\\..\\Resources", "attendanceImg", today)
        os.makedirs(folder_path, exist_ok=True)
        filename = f"{ma_nhan_vien}_{time_now}.jpg"
        file_path = os.path.join(folder_path, filename)
        file_path = os.path.normpath(file_path)
        cv2.imwrite(file_path, frame)
        return file_path

    def checkIn(self, frame, ma_nhan_vien):
        record = self.attendance_repo.getTodayRecord(ma_nhan_vien)
        if record is None:
            path = self.save_attendance_img(frame, ma_nhan_vien)
            self.attendance_repo.insertCheckin(ma_nhan_vien, path)
            print("checkin")
        elif record[3] is None:
            path = self.save_attendance_img(frame, ma_nhan_vien)
            self.attendance_repo.updateCheckout(ma_nhan_vien, path)
            print("Checkout")
        else: print(record[3])

    def getAttendanceYearByEmployee(self, employee):
        return self.attendance_repo.getAttendanceYearById(employee.ma_nhan_vien)

    def getAttendanceByEmployee(self, employee):
        return self.attendance_repo.findByEmployeeId(employee.ma_nhan_vien)