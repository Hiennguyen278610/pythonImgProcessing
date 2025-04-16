# I. Linh tinh

## 1. Về Package view
### a. Giải thích hoạt động của `updateDataTable`

**Chức năng:**  
`updateDataTable(self, data)` là phương thức của lớp `DataTable` dùng để cập nhật lại toàn bộ dữ liệu hiển thị trên bảng (table) khi có dữ liệu mới.

**Cách hoạt động:**
1. Nhận vào một danh sách dữ liệu mới (`data`), thường là list các đối tượng (ví dụ: Employee, Contract, ...).
2. Gán dữ liệu này vào thuộc tính `self.data`.
3. Đặt lại dòng đang chọn (`self.selectedRow = None`).
4. Gọi `self.refreshTable()` để vẽ lại toàn bộ bảng với dữ liệu mới.

**Mã nguồn:**
```python
def updateDataTable(self, data):
    self.data = data
    self.selectedRow = None
    self.refreshTable()
```

---

### Khi nào và ai sẽ gọi `updateDataTable`?

- **Khi nào:**  
  - Khi bạn muốn hiển thị dữ liệu mới lên bảng, ví dụ sau khi tìm kiếm, lọc, thêm, sửa, xóa hoặc tải lại dữ liệu từ database.
  - Sau khi controller đã xử lý xong và trả về dữ liệu (list object) cho view.

- **Ai gọi:**  
  - Thường là các lớp View/Panel (ví dụ: `EmployeePanel`, `ContractPanel`) sẽ gọi.
  - Khi controller trả về dữ liệu mới, View sẽ gọi `datatable.updateDataTable(data)` để cập nhật giao diện.

---

### Ví dụ luồng sử dụng

Giả sử bạn có một panel quản lý nhân viên:

```python
# Trong EmployeePanel
def refresh(self):
    data = self.controller.getAllEmployees()  # Controller trả về list Employee
    self.dataTable.updateDataTable(data)      # Cập nhật lại bảng
```

Hoặc khi tìm kiếm:

```python
def on_search(self, keyword):
    data = self.controller.searchEmployees(keyword)
    self.dataTable.updateDataTable(data)
```

---

### Tổng kết

- `updateDataTable` là cầu nối giữa dữ liệu (controller trả về) và giao diện bảng.
- Được gọi bởi View/Panel mỗi khi cần cập nhật lại dữ liệu hiển thị trên bảng.
- Đảm bảo bảng luôn hiển thị đúng dữ liệu mới nhất từ controller.