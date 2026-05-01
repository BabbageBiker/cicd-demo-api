# CICD Demo API

Personal project built for CS-499 Special Problems.
Containerized REST API built using Python and FastAPI.
Backed with a PostgreSQL database.
Automated Gitlab CI/CD pipeline.

## Tech Stack (requirements.txt)
- **Python / FastAPI** - Backend REST API
- **PostgreSQL** - Relational DB
- **SQLAlchemy** - ORM for DB interactions (Object-Relational Mapping)
- **Docker / Docker compose** - Containerization + orchestration
- **GitLab CI/CD** - Automated pipeline for lint, test, build
- **pytest** - Automated testing
- **flake8** - Linting code formatting/style

## Project Structure
cicd-demo-api/
|-- main.py #
|-- test_main.py #
|-- database.py #
|-- models.py #
|-- schemas.py #
|-- docker-compose.yml #
|-- Dockerfile #
|-- .gitlab-ci.yml #
|-- requirements.txt #

## API Endpoints
Method: GET, Endpoint: '/', Description: Confirms API is running
Method: GET, Endpoint: '/tasks', Description: Returns all tasks stored in the DB
Method: POST, Endpoint: '/tasks', Description: Creates and stores a new task in the DB
Method: GET, Endpoint: '/tasks/{id}', Description: Returns a single task in the DB by ID, 404 if not found
Method: DELETE, Endpoint: '/tasks/{id}', Description: Deletes a single task by ID, 404 if not found

## Running Local

### Prerequisites
- Docker Desktop
- Python 3.12+
- WSL2 (Windows)

### Set-up:
```bash
# cloning the repo:
git clone https://github.com/BabbageBiker/cicd-demo-api.git
cd cicd-demo-api

# create and activate the virtual environment:
python3 -m venv venv
source venv/bin/activate

# install dependencies:
pip install -r requirements.txt
```

### Run with Docker (w/ Docker Desktop running)
```bash
docker compose up --build
```

Interactive API visible at 'https://localhost:8000/docs'

### Testing:
```bash
pytest -v
```

## CI/CD Pipeline
Each time a push is made to GitLab, three stage pipeline is triggered:
1. **Lint** - uses flake8 to verify the code style/formatting across all Python files
2. **Test** - uses pytest to run all tests against a test PostgreSQL service, in container
3. **Build** - Docker will build the app image, verify its packages

## Docker Containers
Runs as two seperate Docker containers, that are orchestrated using Docker Compose:
1. **app** - container for FastAPI application
2. **db** - container for PostgreSQL database
Both containers communicate using Dockers internal network using the service name 'db' as the hostname.
