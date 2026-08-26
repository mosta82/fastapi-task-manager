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

##  Running with Docker (Recommended)

If you have Docker installed on your computer, you can run the app with a single command:

```bash
docker-compose up --build

Then open your browser and go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Running Locally (Without Docker)
1. Clone the repository:

git clone https://github.com/mosta82/fastapi-task-manager.git
cd fastapi-task-manager

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate  # On Windows

3. Install dependencies:
pip install -r requirements.txt

4. Run the FastAPI server:
uvicorn main:app --reload

5. Open API Documentation:
Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

6. Running Tests
To run the automated test suite, use pytest:
pytest
