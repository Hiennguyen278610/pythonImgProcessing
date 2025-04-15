SHOW DATABASES;
DROP DATABASE IF EXISTS FaceRecognition;
CREATE DATABASE IF NOT EXISTS FaceRecognition;

USE FaceRecognition;

CREATE TABLE IF NOT EXISTS Employee (
    employeeID INT AUTO_INCREMENT PRIMARY KEY,
    managerID INT,
    roleID INT,
    name VARCHAR(100) NOT NULL,
    dob DATE,
    phone VARCHAR(15) NOT NULL,
    address VARCHAR(255),
    gender VARCHAR(10),
    startDate DATE,
    FOREIGN KEY (managerID) REFERENCES Employee(employeeID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Contract (
    contractID INT AUTO_INCREMENT PRIMARY KEY,
    employeeID INT NOT NULL,
    term VARCHAR(100) NOT NULL,
    signingDate DATE NOT NULL,
    salary DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID) ON DELETE CASCADE
);

INSERT INTO Employee (employeeID, managerID, roleID, name, dob, phone, address, gender, startDate)
VALUES  (1, NULL, 1, 'Admin User', '1990-01-01', '0123456789', 'Hà Nội', 'Nam', '2020-01-01'),
        (2, 1, 2, 'Nguyễn Văn A', '1995-05-15', '0987654321', 'Hồ Chí Minh', 'Nam', '2021-03-15'),
        (3, 1, 2, 'Trần Thị B', '1998-08-22', '0909123456', 'Đà Nẵng', 'Nữ', '2022-05-10');

-- Thêm dữ liệu mẫu
INSERT INTO Contract (employeeID, term, signingDate, salary)
VALUES  (1, '12 tháng', '2023-01-01', 15000000),
        (2, '6 tháng', '2023-03-15', 12000000),
        (3, '24 tháng', '2022-08-10', 10000000);

SELECT * FROM Employee;