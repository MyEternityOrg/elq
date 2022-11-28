echo off
git clone https://github.com/MyEternityOrg/elq.git
cd elq
git pull
python -m venv venv
venv\scripts\python.exe -m pip install --upgrade pip
venv\Scripts\pip install -r requirements.txt
venv\Scripts\pip install win32printing
IF NOT EXIST .env copy .env.sample .env
venv\scripts\python.exe manage.py migrate
venv\scripts\python.exe manage.py init
venv\Scripts\python manage.py runserver
