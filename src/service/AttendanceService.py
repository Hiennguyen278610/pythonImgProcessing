import face_recognition
import cv2
import os
import pickle
from datetime import datetime
from src.model.repository.AttendanceRespository import AttendanceRespository
from src.model.repository.EmployeeRespository import EmployeeRepository

class AttendanceService:
    def __init__(self):
        self.attendance_repo = AttendanceRespository()
        self.employee_repo = EmployeeRepository()
        self.known_face_encodings = []
        self.known_face_id = []

    def load_known_faces(self):
        employees = self.employee_repo.findAll()
        for employee in employees:
            path = os.path.join("../../../Resources/faceImg/", employee.urlImage)
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                self.known_face_encodings.append(encoding[0])
                self.known_face_id.append(employee.id)
        encodeWithId = [self.known_face_encodings, self.known_face_id]
        with open("../../Encodings/EncodeFile.p", 'wb') as file:
            pickle.dump(encodeWithId, file)

    def add_new_face(self, new_employee):
        try:
            with open("../../Encodings/EncodeFile.p", 'rb') as file:
                encodeWithId = pickle.load(file)
                known_encodings, known_ids = encodeWithId
        except:
            known_encodings, known_ids = [], []
        path = os.path.join("../../../Resources/faceImg/", new_employee.urlImage)
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

    def recognize_and_mark_attendance(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            id = None
            distance = face_recognition.face_distance(self.known_face_id, self.known_face_id)
            if True in matches and distance < 0.3:
                first_match_index = matches.index(True)
                id = self.known_face_id[first_match_index]

                now = datetime.now()

        return id


    def get_employee_attendance(self, frame):
        id = self.recognize_and_mark_attendance(frame)
        employee_attendance = self.employee_repo.findByID(id)
        return employee_attendance