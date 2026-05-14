# CCTV Asset Management System - Backend

This is the Django backend for the CCTV Asset Management System.

## Prerequisites

- Python 3.10+
- PostgreSQL
- pip (Python package manager)

## Setup Instructions

1.  **Navigate to the backend directory:**
    ```bash
    cd backend_django
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Database Configuration:**
    -   Ensure PostgreSQL is running.
    -   Create a database named `cctv`.
    -   The current settings in `core/settings.py` use the following credentials:
        -   **Name:** `cctv`
        -   **User:** `postgres`
        -   **Password:** `9976` (Update in `settings.py` if different)
        -   **Host:** `localhost`
        -   **Port:** `5432`

6.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Create a Superuser (Optional):**
    ```bash
    python manage.py createsuperuser
    ```

## Running the Server

To start the development server, run:
```bash
python manage.py runserver
```
The backend will be available at `http://127.0.0.1:8000/`.

## API Documentation
The system uses Django REST Framework. Once the server is running, you can access the admin interface at `http://127.0.0.1:8000/admin/`.


Backend code run for update after 


# 1. Install missing packages
.\venv\Scripts\pip.exe install Pillow openpyxl

# 2. Run migrations
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate

# 3. Start the server
.\venv\Scripts\python.exe manage.py runserver 5000
