# FastAPI Task Manager API

A secure and robust Task Management RESTful API built with **FastAPI**, **SQLite**, and **SQLAlchemy**. It includes user authentication, task CRUD operations, pagination, status filtering, and full **Docker** support.

---

## 🚀 Features

* **User Authentication:** Secure signup and login using JWT (JSON Web Tokens) and OAuth2.
* **Task Management (CRUD):** Create, read, update, and delete tasks associated with specific users.
* **Pagination & Filtering:** Retrieve tasks efficiently with `skip`, `limit`, and completion status filters (`completed`).
* **Dockerized:** Easily run the entire application using Docker and Docker Compose.
* **Automated CI/CD:** Integrated with GitHub Actions for automated testing (`pytest`).

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** FastAPI
* **Database:** SQLite (SQLAlchemy ORM)
* **Containerization:** Docker & Docker Compose
* **Testing:** Pytest, GitHub Actions

---

## 🐳 Running with Docker (Recommended)

If you have Docker installed on your computer, you can run the app with a single command:

```bash
docker-compose up --build
Then open your browser and go to: http://127.0.0.1:8000/docs

⚙️ Running Locally (Without Docker)
Clone the repository:

Bash
git clone [https://github.com/mosta82/fastapi-task-manager.git](https://github.com/mosta82/fastapi-task-manager.git)
cd fastapi-task-manager
Create and activate a virtual environment:

Bash
python -m venv venv
venv\Scripts\activate  # On Windows
Install dependencies:

Bash
pip install -r requirements.txt
Run the FastAPI server:

Bash
uvicorn main:app --reload
Open API Documentation:

Swagger UI: http://127.0.0.1:8000/docs

🧪 Running Tests
To run the automated test suite, use pytest:

Bash
pytest
