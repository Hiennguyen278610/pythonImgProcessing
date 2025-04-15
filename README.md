# I. Quy trình làm việc:
## 1. Cập nhật thư viện nếu có thay đổi:
```bash
python -m pip install -r requirements.txt
```

# Cấu trúc cây thư mục: 
## Demo
    src/view/
    ├── component/
    │   ├── table/
    │   │   ├── DataTable.py        # Bảng dữ liệu tái sử dụng
    │   │   └── TableCell.py        # Tùy biến cell hiển thị 
    │   ├── toolbar/
    │   │   ├── FilterToolbar.py    # Thanh công cụ lọc và tìm kiếm
    │   │   └── CRUDToolbar.py      # Thanh công cụ CRUD
    │   └── EntityFrame.py          # Khung chứa các thành phần
    ├── panel/
    │   ├── BasePanel.py            # Panel cơ sở cho các đối tượng
    │   ├── EmployeePanel.py        # Panel cụ thể cho Employee
    │   └── ContractPanel.py        # Panel cụ thể cho Contract
    └── dialog/                     # (để sau)
