set APP_NAME=ncrePay
python manage.py makemigrations %APP_NAME%
python manage.py migrate
PAUSE