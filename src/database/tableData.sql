DROP DATABASE IF EXISTS facerecognition;
CREATE DATABASE IF NOT EXISTS facerecognition;
USE facerecognition;

CREATE TABLE nhan_vien (
    ma_nhan_vien INT AUTO_INCREMENT PRIMARY KEY,
    ma_ngql INT,
    ho_ten_nhan_vien VARCHAR(100) not null,
    ngay_sinh DATE not null,
    so_dien_thoai VARCHAR(15) not null,
    dia_chi VARCHAR(100) not null,
    gioi_tinh enum("nam", "nu") not null,
    ngay_vao_lam DATE not null,
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

CREATE TABLE phan_cong (
    ma_nhan_vien int not null,
    ma_chuc_vu int not null,
    PRIMARY KEY (ma_nhan_vien, ma_chuc_vu)
);

INSERT INTO phong (ma_truong_phong, ten_phong) VALUES
(1, 'Phòng Nhân sự'),
(2, 'Phòng Kỹ thuật'),
(3, 'Phòng Kinh doanh');

INSERT INTO chuc_vu (ma_chuc_vu, ma_phong, ten_chuc_vu) VALUES
(1, '1', 'Trưởng phòng'),
(2, '1', 'Nhân viên hành chính'),
(3, '2', 'Kỹ sư phần mềm'),
(4, '3', 'Nhân viên kinh doanh'),
(5, '2', 'Kế toán'),
(6, '3', 'Chuyên viên marketing');

INSERT INTO nhan_vien (ma_ngql, ho_ten_nhan_vien, ngay_sinh, so_dien_thoai, dia_chi, gioi_tinh, ngay_vao_lam, url_image) VALUES
(NULL, 'Nguyễn Thanh Nhàn', '2005-10-16', '0847979732', '3C Đường Trần Phú, Quận 5', 'nam', '2010-01-15', 'messi.jpg'),
(1, 'Nguyễn Hoàng Anh', '2005-11-26', '0912345678', '878 Đường Nguyễn Trãi, Quận ', 'nam', '2015-06-01', 'ronaldo.jpg'),
(1, 'Nguyễn Thanh Hiền', '2005-10-10', '0923456789', '29A Đường Cao Thắng, Quận 3', 'nam', '2018-03-10', 'hien.jpg');

INSERT INTO hop_dong (ma_nhan_vien, thoi_han, ngay_ky, muc_luong) VALUES
(1, '3 năm', '2020-01-01', 15000000.00),
(2, '1 năm', '2022-07-15', 12000000.00),
(3, '2 năm', '2021-09-10', 13000000.00);
INSERT INTO cham_cong
  (ma_nhan_vien, ngay_cham_cong, gio_vao, gio_ra, img_checkin, img_checkout)
VALUES
  (1,
   '2025-04-13',
   '08:00:00',
   '17:00:00',
   'src/../Resources/attendanceImg/2025-04-22/1_00-48-32.jpg',
   'src/../Resources/attendanceImg/2025-04-22/1_00-48-32.jpg'
  );


INSERT INTO phan_cong(ma_nhan_vien, ma_chuc_vu) values
(1, 1),
(2, 3),
(3, 4);

INSERT INTO tai_khoan (ma_nhan_vien, username, password) VALUES
(1, 'abc', 'admin');
alter table chuc_vu
    add constraint foreign key (ma_phong) references phong(ma_phong);

alter table nhan_vien
    add constraint foreign key (ma_ngql) references nhan_vien(ma_nhan_vien);

alter table cham_cong
    add constraint foreign key (ma_nhan_vien) references nhan_vien(ma_nhan_vien);

alter table hop_dong
    add constraint foreign key (ma_nhan_vien) references nhan_vien(ma_nhan_vien);

alter table phan_cong
    add constraint foreign key (ma_chuc_vu) references chuc_vu(ma_chuc_vu),
    add constraint foreign key (ma_nhan_vien) references nhan_vien(ma_nhan_vien);

select * from nhan_vien;
select * from phong;
select * from chuc_vu;
select * from hop_dong;
select * from cham_cong;

SELECT
    nv.ma_nhan_vien, nv.ma_ngql,
    pc.ma_chuc_vu,
    nv.ho_ten_nhan_vien, nv.ngay_sinh, nv.so_dien_thoai,
    nv.dia_chi, nv.gioi_tinh, nv.ngay_vao_lam, nv.url_image
FROM nhan_vien nv
INNER JOIN phan_cong pc ON nv.ma_nhan_vien = pc.ma_nhan_vien