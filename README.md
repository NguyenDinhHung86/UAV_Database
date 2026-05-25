# 🚁 UAV Database & RF Analyzer

Ứng dụng quản lý cơ sở dữ liệu UAV tích hợp công cụ mô phỏng và so sánh tín hiệu RF (Vô tuyến). Được xây dựng bằng Python và PyQt6.

## ✨ Tính năng chính
- **Quản lý danh sách UAV:** Thêm, sửa, xóa thông tin chi tiết về các loại drone (thông số kỹ thuật, hãng sản xuất, năm).
- **Phân tích tín hiệu RF:** Mô phỏng biểu đồ mật độ phổ năng lượng (PSD) và Spectrogram (STFT) cho từng loại UAV dựa trên tần số và băng thông.
- **So sánh UAV:** Cho phép chọn tối đa 6 UAV để so sánh trực quan các thông số kỹ thuật và phổ RF trên cùng một biểu đồ.
- **Giao diện hiện đại:** Chế độ Dark Mode tối ưu cho kỹ sư, sử dụng framework PyQt6 mượt mà.

## 🚀 Cài đặt

1. Đảm bảo bạn đã cài đặt Python 3.8+.
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠 Cách sử dụng

Chạy ứng dụng thông qua file `run.py`:
```bash
python run.py
```

## 📂 Cấu trúc thư mục
- `main.py`: Giao diện người dùng và logic chính.
- `database.py`: Xử lý lưu trữ dữ liệu (JSON).
- `uav_model.py`: Định nghĩa cấu trúc dữ liệu UAV.
- `run.py`: Điểm khởi chạy ứng dụng.

## 📝 Ghi chú
Dữ liệu ban đầu sẽ tự động được khởi tạo (Seed data) nếu file `uav_data.json` chưa tồn tại.