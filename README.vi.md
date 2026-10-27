# Awesome Open WebUI Stack

[English](README.md) | **Tiếng Việt**

Thư viện cộng đồng giúp bạn tìm tools, functions, pipes, integrations và stack tham khảo cho Open WebUI.

**[Mở catalog](https://newnol.github.io/awesome-openwebui-stack/)** | **[Bắt đầu từ đây](START-HERE.vi.md)** | **[Đọc trên GitHub](catalog/README.md)**

## Chọn đúng tiện ích

Tìm theo nhu cầu, lọc theo loại và bằng chứng, so sánh tối đa ba mục, rồi đọc hướng dẫn từ tác giả gốc. Mỗi mục nêu phụ thuộc, giới hạn tương thích, rủi ro và ngày kiểm tra nguồn.

**Đã xem nguồn không có nghĩa là đã chạy thử hay kiểm toán bảo mật.** Các mục chưa có implementation được giữ lại kèm cảnh báo và ẩn mặc định. Repo này không phải cửa hàng cài đặt tự động.

## Đóng góp

Bạn có thể gửi biểu mẫu issue mà không cần sửa mã. Khi gửi PR, sửa `data/catalog.json` và chạy `node scripts/catalog.mjs` để sinh lại catalog và các trang phân loại. Xem [CONTRIBUTING.md](CONTRIBUTING.md) và [tài liệu bảo trì](docs/catalog-maintenance.md).

## Xem trên máy

```bash
python3 -m http.server 8000
```

Mở `http://localhost:8000`. Giao diện catalog và metadata hiện bằng tiếng Anh; hướng dẫn nhập môn có bản tiếng Việt.

## Phạm vi và giấy phép

Repo dùng [MIT](LICENSE). Từng dự án, model và dịch vụ được dẫn có giấy phép hoặc điều khoản riêng. Đây là dự án cộng đồng, không đại diện cho Open WebUI.
