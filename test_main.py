import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base
from main import get_db

# When testing, use a separate SQLite database for test populating
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine)


# create tables in test db
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# overide app db session  with test db session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Test functions


# checks that root endpoint responds and contains correct status code
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# create test task, check that title and description are correct, completed = false, and contains correct status code
def test_create_task():
    response = client.post("/tasks", json={"title": "TestTask", "description": "Test description of TestTask."})
    assert response.status_code == 201
    assert response.json()["title"] == "TestTask"
    assert response.json()["completed"] is False


# creates 2 test tasks, calls GET /tasks and verifies that 2 tasks come back
def test_get_tasks():
    client.post("/tasks", json={"title": "Task1"})
    client.post("/tasks", json={"title": "Task2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


# create test task, verify that it can be fetched by ID correctly
def test_get_task():
    created = client.post("/tasks", json={"title": "TaskToGet"})
    task_id = created.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "TaskToGet"


# test GET with a task that does not exist
def test_get_task_not_found():
    response = client.get("/tasks/10000")
    assert response.status_code == 404


# create test task, verify that it can be deleted correctly using its id
def test_delete_task():
    created = client.post("/tasks", json={"title": "Task To Be Deleted"})
    task_id = created.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204


# test DELETE with a task that does not exist
def test_delete_task_not_found():
    response = client.delete("/tasks/10000")
    assert response.status_code == 404
