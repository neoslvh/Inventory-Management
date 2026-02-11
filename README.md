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
