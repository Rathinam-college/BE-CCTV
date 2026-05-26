@echo off
echo 1. Deleting broken virtual environment...
if exist .venv rmdir /s /q .venv

echo 2. Creating a new virtual environment...
python -m venv .venv

echo 3. Activating and installing requirements...
call .venv\Scripts\activate
pip install -r requirements.txt

echo 4. Starting the backend server...
python manage.py runserver 5000
pause
