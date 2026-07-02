@echo off
echo Installing Pillow to fix ImageField error...
python -m pip install Pillow

echo.
echo Running migrations...
python manage.py makemigrations cctv
python manage.py migrate

echo.
echo Done! Please check the output above for any errors.
pause
