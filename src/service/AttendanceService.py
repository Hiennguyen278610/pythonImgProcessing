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
        employees = self.employee_repo.findAll()

        # Get the absolute path to the project directory
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # Create resources directory if it doesn't exist
        resources_dir = os.path.join(project_dir, "Resources")
        faceimg_dir = os.path.join(resources_dir, "faceImg")

        os.makedirs(resources_dir, exist_ok=True)
        os.makedirs(faceimg_dir, exist_ok=True)

        for employee in employees:
            # This fixes the path to just use faceImg once (not twice)
            path = os.path.join(project_dir, "Resources", "faceImg", employee.url_image.replace("faceImg\\", ""))
            path = os.path.normpath(path)

            # Debug output
            print(f"Looking for image at: {path}")

            if not os.path.exists(path):
                print(f"Warning: Image file not found: {path}")
                continue

            try:
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    self.known_face_encodings.append(encoding[0])
                    self.known_face_id.append(employee.ma_nhan_vien)
            except Exception as e:
                print(f"Error processing image {path}: {str(e)}")

        # Save encodings
        encodeWithId = [self.known_face_encodings, self.known_face_id]
        encode_file_path = os.path.join(project_dir, "Resources", "EncodeFile.p")
        encode_file_path = os.path.normpath(encode_file_path)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(encode_file_path), exist_ok=True)

        print(f"Saving encodings to: {encode_file_path}")
        with open(encode_file_path, 'wb') as file:
            pickle.dump(encodeWithId, file)

    def load_file_encode(self):
        try:
            project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            encode_file_path = os.path.join(project_dir, "Resources", "EncodeFile.p")
            encode_file_path = os.path.normpath(encode_file_path)

            print(f"Looking for encodings at: {encode_file_path}")

            if not os.path.exists(encode_file_path):
                print(f"Encodings file not found: {encode_file_path}")
                self.known_face_encodings, self.known_face_id = [], []
                return

            with open(encode_file_path, 'rb') as file:
                encodeWithId = pickle.load(file)
                self.known_face_encodings, self.known_face_id = encodeWithId
                print(f"Loaded {len(self.known_face_encodings)} face encodings")
        except Exception as e:
            self.known_face_encodings, self.known_face_id = [], []
            print(f"No encodings loaded: {str(e)}")

    def add_new_face(self, new_employee):
        try:
            with open("../../Resources/EncodeFile.p", 'rb') as file:
                encodeWithId = pickle.load(file)
                known_encodings, known_ids = encodeWithId
        except:
            known_encodings, known_ids = [], []
        path = os.path.join("../../../Resources/", new_employee.urlImage)
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
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        today = datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H-%M-%S")
        folder_path = os.path.join(project_dir, "Resources", "attendanceImg", today)
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