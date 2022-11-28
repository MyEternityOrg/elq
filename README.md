## Электронная очередь

### Система регистрации чеков в электронной очереди производства.

Основные системные требования:

* Python 3.10
* Django 4
* Зависимости (Python) из requirements.txt

* Ниже показаны примеры установки под разные виды ОС

## Установка необходимого ПО для Ubuntu

#### Для работы подсистемы печати потребуется доустановить дполнительные пакеты:

```
apt install gcc
apt install libcups2-dev
apt install python3-dev
apt install python3-setuptools
```

#### Обновляем информацию о репозиториях

```
apt update
```

#### Установка дополнительных пакетов

```
apt install python3-pip
apt install screen
apt install git-core
apt install python3-venv
```

#### Настраиваем виртуальное окружение

Создаем и активируем виртуальное окружение:

```
cd /opt
git clone https://github.com/MyEternityOrg/elq.git
cd /elq
python3 -m venv venv
venv/bin/python3 -m pip install --upgrade pip
venv/bin/pip install -r requirements.txt
venv/bin/pip install pycups
cp .env.sample .env
venv/bin/python3 manage.py migrate
venv/bin/python3 manage.py init
```

#### Суперпользователь

```
init: Создает суперпользователя shop с паролем 123
```

### Запуск проекта

```
venv/bin/python3 manage.py runserver
```

### После этого в браузере можно ввести ip-адрес сервера и откроется проект.

#### Обновление проекта из Git:

```
cd /opt/elq
git pull
venv/bin/python3 -m pip install --upgrade pip
venv/bin/pip install -r requirements.txt
venv/bin/python3 manage.py migrate
```

### Установка для Windows.

#### В качестве примера можно взять elq_win.cmd из конерневой директории проекта.

Установка вручную:

#### В нужном каталоге открываем командную строку.

```
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
```