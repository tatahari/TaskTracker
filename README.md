# Task Tracker Application

A production-ready task tracking application built with FastAPI, HTMX, Alpine.js, and Tailwind CSS. Containerized with Podman.

## Features
- **CRUD Operations**: Create, Read, Update, and Delete tasks.
- **Modern UI**: Responsive dashboard with sorting and filtering.
- **HTMX Powered**: Smooth interactions without full page reloads.
- **Export**: One-click export to CSV and Excel (.xlsx).
- **Persistence**: SQLite database mounted as a volume for easy backups.
- **Production Ready**: Includes health checks and optimized Dockerfile.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: HTMX, Alpine.js, Tailwind CSS
- **Database**: SQLite
- **Containerization**: Podman / Docker

## Quick Start (Podman)

1. Ensure you have Podman and `podman-compose` installed.
2. Clone the repository and navigate to the root directory.
3. Run the following command:
   ```bash
   podman-compose up -d
   ```
4. Access the application at [http://localhost:8000](http://localhost:8000).
   - **Username**: `admin`
   - **Password**: `password`

## Manual Setup (Local Development)

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure
- `app/`: Source code for the FastAPI backend and templates.
- `app/models.py`: Database schema.
- `app/routers/`: API and UI endpoints.
- `app/templates/`: HTML templates using Jinja2.
- `Dockerfile`: Container image definition.
- `podman-compose.yml`: Multi-container orchestration.

## License
MIT
