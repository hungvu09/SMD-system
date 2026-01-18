# SMD-system


### Cấu trúc dự án (src/)
src/                                # Thư mục chính chứa toàn bộ mã nguồn hệ thống SMD
│
├── config/                         # Cấu hình hệ thống
│   ├── exception.py                # Các exception tùy chỉnh
│   └── settings.py                 # Config chung (Supabase URL, keys, env vars, constants)
│
├── controllers/                    # Điều khiển chức năng (API handlers / route logic)
│   ├── feedback_control.py
│   ├── search_control.py
│   ├── system_control.py
│   └── user_controller.py
│
├── data/                           # Kết nối và helper database
│   └── supa.py                     # Supabase client wrapper
│
├── infrastructure/                 # Tích hợp bên ngoài / adapters
│   └── ai/                         # Module AI
│       ├── change_detec.py         # Phát hiện thay đổi ngữ nghĩa
│       ├── summary.py              # Tóm tắt nội dung
│       ├── syl_analys.py           # Phân tích syllabus (CLO-PLO, consistency check)
│       └── ai_crawler.py           # Thu thập dữ liệu tham khảo
│
├── middleware/                     # Middleware (auth, RBAC, logging,...)
│   ├── auth_required.py
│   └── role_required.py
│
├── object/
│   └── entities/                   # Domain models / Business entities
│       ├── academic.py
│       ├── clo.py
│       ├── course_relation.py      # Mối quan hệ môn học (tiên quyết, song hành, bổ trợ)
│       ├── feedback.py
│       ├── hod.py
│       ├── lecturer.py
│       ├── model_user.py           # Model người dùng
│       ├── notifications.py
│       ├── plo.py
│       ├── rector.py
│       ├── student.py
│       ├── syllabus.py             # Giáo trình chính
│       ├── syllabus_ver.py         # Phiên bản giáo trình
│       └── workflow.py             # Quy trình phê duyệt (approval workflow)
│
├── repositories/                   # Data access layer (CRUD cho từng entity)
│   ├── feedback_repo.py
│   ├── syllabus_repo.py
│   └── user_repo.py
│
├── schemas/                        # Pydantic schemas cho request/response
│   ├── syl_create.py               # Schema tạo syllabus
│   ├── syl_response.py             # Schema trả về chi tiết
│   └── syl_update.py               # Schema cập nhật syllabus
│
├── services/                       # Business logic / use cases
│   ├── ai_service.py               # Orchestration các tác vụ AI
│   └── auth_service.py             # Xử lý đăng nhập, token, role
│
├── tests/                          # Unit & integration tests
│   └── test_ai.py                  # Test các module AI (có thể thêm test khác sau)
│
├── website/                        # Module web (templates, static, routes cũ)
│   ├── init.py                 # Package initializer cho website
│   ├── auth.py                     # Xử lý auth (có thể là route hoặc helper cũ)
│   ├── views.py                    # Chứa các route (đang chuyển dần sang controllers)
│   ├── main.py                     # Entry point chạy ứng dụng Flask
│   │
│   ├── static/                     # Tài nguyên tĩnh (CSS, JS, images)
│   │   └── JS/
│   │       └── index.js
│   │
│   └── templates/                  # Jinja2 templates (Flask rendering)
│       ├── admin.html
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── signup.html
│       └── student.html