Inventory Management System



A production-ready Flask-based multi-warehouse inventory and purchasing system with REST APIs, Swagger documentation, real-time updates, and Redis caching.

Designed for small-to-medium teams that require accurate stock visibility, warehouse tracking, and scalable backend architecture.

✨ Core Features

Role-based authentication (Flask-Login)

Secure admin panel (Flask-Admin)

Multi-warehouse stock management

FIFO inventory movement (IN, OUT, TRANSFER)

Product search by name, SKU, or barcode

Batch & expiry tracking

Low-stock alert API with caching

Excel export reporting

Swagger API documentation (Flasgger)

Real-time updates via Flask-SocketIO

Redis caching layer

Pytest test suite with SQLite in-memory DB

🏗 Architecture Overview

MVC-style modular Flask blueprint structure

RESTful API endpoints under /api

PostgreSQL for persistence

Redis for caching and SocketIO message queue

Environment-driven configuration

Migration-controlled schema management

🛠 Tech Stack

Backend:

Python 3.10+

Flask

Flask-SQLAlchemy

Flask-Migrate

Flask-Admin

Flask-RESTful

Flasgger

Flask-SocketIO

Infrastructure:

PostgreSQL

Redis

Gunicorn (production WSGI server)

Eventlet (async support)

Testing:

Pytest

Coverage

📂 Project Structure
app/
 ├── api/
 ├── auth/
 ├── inventory/
 ├── models/
 ├── reports/
 ├── docs/
 ├── static/
 └── templates/

migrations/
test/
manage.py
config.py
wsgi.py

🚀 Quick Start (Local Development)
1. Clone repository
git clone <repo-url>
cd Inventory-Management-main

2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Setup environment variables

Create .env:

FLASK_APP=manage.py
FLASK_ENV=development
SECRET_KEY=change-me
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:pass@localhost/invms
REDIS_URL=redis://127.0.0.1:6379/0
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=StrongPass123

5. Run migrations
flask --app manage.py db upgrade

6. Start development server
python manage.py


App runs at:

http://localhost:5000

🐳 Docker Deployment
Example Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "wsgi:app"]

Build image
docker build -t inventory-app .

Run container
docker run -p 5000:5000 \
  -e SECRET_KEY=change-me \
  -e SQLALCHEMY_DATABASE_URI=postgresql://user:pass@db/invms \
  -e REDIS_URL=redis://redis:6379/0 \
  inventory-app


For production, use Docker Compose with PostgreSQL + Redis services.

🔄 CI/CD Example (GitHub Actions)

Create .github/workflows/test.yml:

name: CI Pipeline

on:
  push:
    branches: [ main, dev ]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:14
        ports: [5432:5432]
        env:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: pass
          POSTGRES_DB: invms

      redis:
        image: redis:6
        ports: [6379:6379]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest coverage

      - name: Run Tests
        run: pytest

🧪 Testing
pytest


With coverage:

coverage run -m pytest
coverage html

📌 Future Improvements

Sales order module

Purchase order approval workflow

Horizontal scaling with Redis message queue

Advanced analytics dashboard

Full Docker Compose production template

📄 License

MIT License (recommended for open-source portfolio projects)



Hệ thống Quản lý Kho (Inventory Management System)

Một hệ thống quản lý tồn kho và mua hàng đa kho dựa trên Flask, sẵn sàng cho môi trường production, cung cấp REST API, tài liệu Swagger, cập nhật thời gian thực và cơ chế cache bằng Redis.

Được thiết kế cho các nhóm nhỏ đến trung bình cần theo dõi tồn kho chính xác, quản lý nhiều kho hàng và kiến trúc backend có khả năng mở rộng.

✨ Tính năng chính

Xác thực người dùng theo vai trò (Flask-Login)

Trang quản trị bảo mật (Flask-Admin)

Quản lý tồn kho đa kho

Quản lý luân chuyển hàng theo FIFO (Nhập, Xuất, Chuyển kho)

Tìm kiếm sản phẩm theo tên, SKU hoặc mã vạch

Theo dõi lô hàng và hạn sử dụng

API cảnh báo tồn kho thấp có caching

Xuất báo cáo Excel

Tài liệu API bằng Swagger (Flasgger)

Cập nhật thời gian thực với Flask-SocketIO

Lớp cache Redis

Bộ kiểm thử Pytest với SQLite in-memory

🏗 Tổng quan kiến trúc

Cấu trúc Flask dạng modular theo mô hình MVC

API RESTful dưới đường dẫn /api

PostgreSQL làm cơ sở dữ liệu chính

Redis dùng cho caching và message queue của SocketIO

Cấu hình theo biến môi trường

Quản lý thay đổi schema bằng migration

🛠 Công nghệ sử dụng
Backend

Python 3.10+

Flask

Flask-SQLAlchemy

Flask-Migrate

Flask-Admin

Flask-RESTful

Flasgger

Flask-SocketIO

Hạ tầng

PostgreSQL

Redis

Gunicorn (WSGI server cho production)

Eventlet (hỗ trợ async)

Kiểm thử

Pytest

Coverage

📂 Cấu trúc dự án
app/
 ├── api/
 ├── auth/
 ├── inventory/
 ├── models/
 ├── reports/
 ├── docs/
 ├── static/
 └── templates/

migrations/
test/
manage.py
config.py
wsgi.py

🚀 Khởi chạy nhanh (Phát triển local)
Clone repository
git clone <repo-url>
cd Inventory-Management-main

Tạo môi trường ảo
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

Cài đặt thư viện
pip install -r requirements.txt

Thiết lập biến môi trường

Tạo file .env:

FLASK_APP=manage.py
FLASK_ENV=development
SECRET_KEY=change-me
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:pass@localhost/invms
REDIS_URL=redis://127.0.0.1:6379/0
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=StrongPass123

Chạy migration
flask --app manage.py db upgrade

Khởi chạy server
python manage.py


Ứng dụng chạy tại:

http://localhost:5000

🐳 Triển khai bằng Docker
Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "wsgi:app"]

Build image
docker build -t inventory-app .

Chạy container
docker run -p 5000:5000 \
-e SECRET_KEY=change-me \
-e SQLALCHEMY_DATABASE_URI=postgresql://user:pass@db/invms \
-e REDIS_URL=redis://redis:6379/0 \
inventory-app


Đối với môi trường production, nên sử dụng Docker Compose để chạy cùng PostgreSQL và Redis.

🔄 CI/CD (GitHub Actions)

Tạo file .github/workflows/test.yml

Pipeline sẽ:

Khởi tạo PostgreSQL và Redis service

Cài đặt Python 3.11

Cài dependencies

Chạy test bằng Pytest

🧪 Kiểm thử

Chạy test:

pytest


Chạy kèm coverage:

coverage run -m pytest
coverage html

📌 Hướng phát triển tương lai

Module đơn hàng bán (Sales order)

Quy trình phê duyệt đơn mua (Purchase order workflow)

Scale ngang với Redis message queue

Dashboard phân tích nâng cao

Template Docker Compose hoàn chỉnh cho production

📄 Giấy phép

MIT License (phù hợp cho dự án mã nguồn mở / portfolio)
