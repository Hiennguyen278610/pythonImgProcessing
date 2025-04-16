# I. Quy trình làm việc:
## 1. Cập nhật thư viện nếu có thay đổi:
```bash
python -m pip install -r requirements.txt
```

# II. Workflow mô hình MVC: 
Khi người dùng ấn nút "Thêm hợp đồng" (Add Contract), luồng hoạt động giữa các tầng MVC như sau:

---

### 1. View (ContractPanel)
- **Người dùng nhấn nút "Thêm"** trên giao diện `ContractPanel`.
- Hàm `onAdd()` trong `ContractPanel` được gọi.
- Thông thường, một dialog nhập thông tin hợp đồng mới sẽ hiện ra (chưa implement, nhưng về nguyên tắc là vậy).
- Người dùng nhập thông tin và xác nhận lưu.

### 2. Controller (ContractController)
- View lấy dữ liệu từ form nhập và gọi `ContractController.create(contract_data)`.
- Controller nhận dữ liệu, kiểm tra sơ bộ (nếu cần), rồi chuyển tiếp cho Service.

### 3. Service (ContractService)
- Service nhận dữ liệu, kiểm tra tính hợp lệ (validate), có thể xử lý logic nghiệp vụ (ví dụ: kiểm tra nhân viên có tồn tại không).
- Nếu hợp lệ, Service gọi Repository để lưu vào database.

### 4. Model/Repository (ContractRepository)
- Repository thực hiện truy vấn SQL để thêm hợp đồng mới vào bảng `Contract` trong database.
- Nếu thành công, trả về đối tượng Contract vừa tạo (có ID mới).

### 5. Quay lại các tầng trên
- Service trả về kết quả cho Controller.
- Controller trả về cho View.
- View gọi lại `loadData()` để lấy danh sách hợp đồng mới nhất (bao gồm cả hợp đồng vừa thêm).
- Bảng dữ liệu trên giao diện được cập nhật, người dùng thấy hợp đồng mới xuất hiện.

---

### Sơ đồ luồng dữ liệu

```
[User click Add] 
   ↓
[View: ContractPanel.onAdd()]
   ↓
[Controller: ContractController.create()]
   ↓
[Service: ContractService.createContract()]
   ↓
[Repository: ContractRepository.save()]
   ↓
[Database: INSERT]
   ↑
[Repository trả về Contract mới]
   ↑
[Service trả về]
   ↑
[Controller trả về]
   ↑
[View gọi lại loadData() → Controller.getAll() → Service.getAll() → Repository.findAll()]
   ↑
[View cập nhật bảng, hiển thị hợp đồng mới]
```

---

### Tóm tắt từng bước

1. **View**: Hiển thị form nhập, nhận dữ liệu, gọi controller.
2. **Controller**: Nhận dữ liệu, chuyển cho service.
3. **Service**: Kiểm tra, xử lý nghiệp vụ, gọi repository.
4. **Repository**: Thêm vào database, trả về kết quả.
5. **View**: Refresh bảng, hiển thị dữ liệu mới.

---

**Lưu ý:**  
- Mỗi tầng chỉ làm đúng nhiệm vụ của mình, không làm thay việc của tầng khác.
- Việc cập nhật giao diện luôn do View đảm nhận, sau khi nhận dữ liệu mới từ Controller.