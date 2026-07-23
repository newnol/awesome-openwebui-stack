# Awesome Open WebUI Stack

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Checks](https://github.com/newnol/awesome-openwebui-stack/actions/workflows/checks.yml/badge.svg)](https://github.com/newnol/awesome-openwebui-stack/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[English](README.md) · **Tiếng Việt**

Một **bộ sưu tập hướng đến cộng đồng**: các **stack**, **tool**, **function** và **pipe** đã hoàn thiện, đáng biết cho [Open WebUI](https://github.com/open-webui/open-webui). Mỗi mục nên trỏ tới thứ **dùng được ngay hôm nay** (repo, bản phát hành, hoặc bài viết chính thức/cộng đồng)—đây **không phải** repo hướng dẫn để xây tool mới.

1. **Có gì đáng thử?** Các mục được tuyển chọn, mục đích rõ ràng và có liên kết ổn định.
2. **Dùng để làm gì?** Duyệt theo **categories** (mục tiêu) hoặc **catalog** (loại artifact).
3. **Mã nguồn ở đâu?** Chỉ liên kết ra ngoài; mã nguồn nằm ở các repo gốc.

**Tiêu chuẩn để được đưa vào:** stack hoặc tool/function/pipe **đủ hoàn thiện để giới thiệu** (hoặc gắn nhãn trung thực **Beta** / **Không còn bảo trì** kèm bối cảnh). Muốn biết **cách tự viết** tool, pipe hay filter, hãy dùng **[tài liệu Open WebUI](https://docs.openwebui.com/)** và mã nguồn gốc—không phải repo này.

---

## Mục lục

- [Dành cho ai](#dành-cho-ai)
- [Tiêu chí lựa chọn](#tiêu-chí-lựa-chọn)
- [Điều hướng nhanh](#điều-hướng-nhanh)
- [Stack tiêu biểu](#stack-tiêu-biểu)
- [Đóng góp](#đóng-góp)
- [Phạm vi](#phạm-vi)
- [Giấy phép](#giấy-phép)

---

## Dành cho ai

- Người muốn chọn các mẫu đã được kiểm chứng (stack) hoặc add-on cho Open WebUI.
- Tác giả muốn **quảng bá** thứ mình đã phát hành.
- Người đọc muốn so sánh lựa chọn—không phải hướng dẫn "tạo tool đầu tiên" từng bước.

---

## Tiêu chí lựa chọn

Ưu tiên **mã nguồn công khai**, **giấy phép rõ ràng** và **trạng thái chính xác**. Xem [docs/review-criteria.md](docs/review-criteria.md) và [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Điều hướng nhanh

| Duyệt theo | Mô tả |
|-----------|-------|
| [catalog/tools.md](catalog/tools.md) | Tool Python (gọi được từ giao diện) |
| [catalog/functions.md](catalog/functions.md) | Function (filter, action, v.v.) |
| [catalog/pipes.md](catalog/pipes.md) | Pipe (định tuyến model, pipeline tùy biến) |
| [catalog/stacks.md](catalog/stacks.md) | Stack tham chiếu + template |
| [catalog/integrations.md](catalog/integrations.md) | Dịch vụ ngoài và mẫu kết nối |
| [catalog/learning-resources.md](catalog/learning-resources.md) | Tài liệu chính thức và nguồn học bên ngoài |

**Theo mục tiêu:**

| Chủ đề | Tệp |
|--------|-----|
| Lập trình | [categories/coding.md](categories/coding.md) |
| Nghiên cứu | [categories/research.md](categories/research.md) |
| RAG | [categories/rag.md](categories/rag.md) |
| Tự động hóa | [categories/automation.md](categories/automation.md) |
| Năng suất | [categories/productivity.md](categories/productivity.md) |
| Đa tác tử | [categories/multi-agent.md](categories/multi-agent.md) |
| Tự lưu trữ | [categories/self-hosting.md](categories/self-hosting.md) |
| Bảo mật | [categories/security.md](categories/security.md) |

**Stack:** [stacks/openwebui-stack/](stacks/openwebui-stack/) — chỉ mục [stacks/README.md](stacks/README.md).

---

## Stack tiêu biểu

- **[Open WebUI stack](stacks/openwebui-stack/)** — Ví dụ bố cục thiên về Docker Compose (LiteLLM, tìm kiếm, phác thảo RAG). Mỗi README của stack đều có liên kết **GitHub của tác giả**.

---

## Triển khai mà chúng tôi liên kết tới

Các ví dụ của maintainer nằm ở **[openwebui-extension](https://github.com/newnol/openwebui-extension)** — liệt kê trong [catalog/tools.md](catalog/tools.md) và [catalog/pipes.md](catalog/pipes.md).

---

## Đóng góp

Chỉ thêm các mục **đã hoàn thiện**. Xem [CONTRIBUTING.md](CONTRIBUTING.md), [docs/submission-guidelines.md](docs/submission-guidelines.md), [docs/review-criteria.md](docs/review-criteria.md), [docs/category-guide.md](docs/category-guide.md), [docs/faq.md](docs/faq.md). Issue: [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/).

Khi tham gia, bạn đồng ý với [Quy tắc ứng xử](CODE_OF_CONDUCT.md) của chúng tôi.

---

## Phạm vi

| Repo này | Nơi khác |
|----------|----------|
| Mô tả ngắn + liên kết tới sản phẩm **đã phát hành** | Cách tự viết extension → **[docs.openwebui.com](https://docs.openwebui.com/)** |
| Tệp `docker-compose` nhỏ (tùy chọn) đặt cạnh README của stack | Repo hạ tầng lớn chỉ dùng cho production |
| Tuyển chọn & khám phá | Toàn bộ cây mã nguồn tool (repo GitHub riêng) |

---

## Giấy phép

MIT — xem [LICENSE](LICENSE).
