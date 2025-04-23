DROP DATABASE IF EXISTS facerecognition;
CREATE DATABASE IF NOT EXISTS facerecognition;
USE facerecognition;

CREATE TABLE nhan_vien (
    ma_nhan_vien INT AUTO_INCREMENT PRIMARY KEY,
    ma_ngql INT,
    ma_chuc_vu INT not null,
    ho_ten_nhan_vien VARCHAR(100) not null,
    ngay_sinh DATE not null,
    so_dien_thoai VARCHAR(15) not null,
    dia_chi VARCHAR(100) not null,
    gioi_tinh enum("nam", "nu") not null,
    ngay_vao_lam DATE not null,
    trang_thai enum("active", "deleted"),
    url_image VARCHAR(255) not null
);

CREATE TABLE cham_cong (
    ma_nhan_vien INT not null,
    ngay_cham_cong DATE not null,
    gio_vao TIME not null,
    gio_ra TIME,
    img_checkin VARCHAR(255) not null,
    img_checkout VARCHAR(255),
    PRIMARY KEY (ma_nhan_vien, ngay_cham_cong)
);

CREATE TABLE hop_dong (
    ma_hop_dong INT AUTO_INCREMENT PRIMARY KEY,
    ma_nhan_vien INT not null,
    thoi_han VARCHAR(50) not null,
    ngay_ky DATE not null,
    muc_luong DECIMAL(15,2) not null
);

CREATE TABLE phong (
    ma_phong INT AUTO_INCREMENT PRIMARY KEY,
    ma_truong_phong INT,
    ten_phong VARCHAR(100) not null
);

CREATE TABLE chuc_vu (
    ma_chuc_vu INT PRIMARY KEY,
    ma_phong INT not null,
    ten_chuc_vu VARCHAR(50) NOT NULL
);

CREATE TABLE tai_khoan (
    ma_nhan_vien INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (ma_nhan_vien) REFERENCES nhan_vien(ma_nhan_vien)
);


INSERT INTO phong (ma_truong_phong, ten_phong) VALUES
(1, 'Phòng Nhân sự'),
(2, 'Phòng Kỹ thuật'),
(3, 'Phòng Kinh doanh'),
(4, 'Phòng Tài chính'),
(5, 'Phòng Marketing');

INSERT INTO chuc_vu (ma_chuc_vu, ma_phong, ten_chuc_vu) VALUES
(1, '1', 'Trưởng phòng'),
(2, '1', 'Nhân viên hành chính'),
(3, '2', 'Kỹ sư phần mềm'),
(4, '3', 'Nhân viên kinh doanh'),
(5, '4', 'Kế toán'),
(6, '5', 'Chuyên viên marketing');

INSERT INTO nhan_vien (ma_ngql, ma_chuc_vu, ho_ten_nhan_vien, ngay_sinh, so_dien_thoai, dia_chi, gioi_tinh, ngay_vao_lam, trang_thai,url_image) VALUES
(NULL, 1, 'Nguyễn Văn A', '1985-05-20', '0909123456', '123 Đường A, Quận 1', 'nam', '2010-01-15', 'active', 'messi.jpg'),
(1, 3, 'Trần Thị B', '1990-09-12', '0912345678', '456 Đường B, Quận 2', 'nu', '2015-06-01', 'active','goat.jpg'),
(1, 4, 'Lê Văn C', '1992-11-25', '0923456789', '789 Đường C, Quận 3', 'nam', '2018-03-10', 'active','ronaldo.jpg'),
(2, 5, 'Phạm Hồng D', '1988-07-30', '0932123456', '321 Đường D, Quận 4', 'nu', '2012-10-20', 'active','neymar.jpg'),
(3, 6, 'Đỗ Thanh E', '1995-04-18', '0941234567', '654 Đường E, Quận 5', 'nam', '2020-08-05', 'deleted','dimaria.jpg');

INSERT INTO hop_dong (ma_nhan_vien, thoi_han, ngay_ky, muc_luong) VALUES
(1, '3 năm', '2020-01-01', 15000000.00),
(2, '1 năm', '2022-07-15', 12000000.00),
(3, '2 năm', '2021-09-10', 13000000.00),
(4, '5 năm', '2015-03-25', 14000000.00),
(5, '1 năm', '2024-01-10', 12500000.00);

INSERT INTO cham_cong (ma_nhan_vien, ngay_cham_cong, gio_vao, gio_ra, img_checkin, img_checkout) VALUES
(1, '2025-04-13', '08:00:00', '17:00:00', 'scr/../Resources/attendanceImg/2025-04-22/1_00-48-32.jpg', 'scr/../Resources/attendanceImg/2025-04-22/1_00-48-32.jpg'),
(1, '2025-04-14', '08:00:00', '17:00:00', 'images/cc1.jpg', ''),
(1, '2025-04-15', '08:00:00', '17:00:00', 'images/cc1.jpg', ''),
(1, '2025-04-16', '08:00:00', '17:00:00', 'images/cc1.jpg', ''),
(1, '2025-04-17', '08:00:00', '', 'images/cc1.jpg', ''),
(2, '2025-04-13', '08:15:00', '17:10:00', 'images/cc2.jpg', ''),
(3, '2025-04-13', '08:05:00', '17:05:00', 'images/cc3.jpg', ''),
(4, '2025-04-13', '07:55:00', '16:50:00', 'images/cc4.jpg', ''),
(5, '2025-04-13', '08:10:00', '17:20:00', 'images/cc5.jpg', '');


INSERT INTO tai_khoan (ma_nhan_vien, username, password) VALUES
(1, 'abc', 'admin');
alter table chuc_vu
    add constraint foreign key (ma_phong) references phong(ma_phong);

alter table nhan_vien
    add constraint foreign key (ma_chuc_vu) references chuc_vu(ma_chuc_vu),
    add constraint foreign key (ma_ngql) references nhan_vien(ma_nhan_vien);

alter table cham_cong
    add constraint foreign key (ma_nhan_vien) references nhan_vien(ma_nhan_vien);

alter table hop_dong
    add constraint foreign key (ma_nhan_vien) references nhan_vien(ma_nhan_vien);

select * from nhan_vien;
select * from phong;
select * from chuc_vu;
select * from hop_dong;
select * from cham_cong;