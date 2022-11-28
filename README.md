# Электронная очередь

### Система регистрации чеков в электронной очереди производства.

Основные системные требования:

* Python 3.10 (Windows: https://www.python.org/)
* Git (Windows: https://github.com/git-guides/install-git)
* Зависимости (Python) из requirements.txt
* Дополнительные библиотеки для работы печати (в зависимости от типа ОС)

## Установка необходимого ПО для Ubuntu 22.04

#### Обновляем информацию о репозиториях

```
sudo su -
apt update
```

#### Установка дополнительных пакетов

```
apt install python3-pip
apt install screen
apt install git-core
apt install python3-venv
```

#### Для работы подсистемы печати потребуется установить дополнительные пакеты:

```
apt install gcc
apt install libcups2-dev
apt install python3-dev
apt install python3-setuptools
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
venv/bin/python3 manage.py runserver
```

## Установка для Windows.

В качестве примера можно взять elq_win.cmd из корневой директории проекта.

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

# Дополнительная настройка проекта

### api_key

Для ограничения доступа к post интерфейсу получения кассовых чеков можно задать свой собственный api_key, в файле .env

```
API_KEY = 'secret_key_here'
```

#### Суперпользователь

```
init: Создает суперпользователя shop с паролем 123
```

### api_import_receipts

В папке examples проекта - приложение сборщик данных по продажам из касс Set Reatail 10 (Crystal)

* api - Адрес интерфейса.
* api_key - Ключ доступа.
* timer - Интервал опроса касс из списка (cashes) в секундах.
* cashes - массив кассовых терминалов.

settings.json

```
{
	"api": "http://127.0.0.1:8000//devices/import_receipt/",
	"api_key": "secret_key_here",
	"timer": 3,
	"cashes": [
		{
			"sql_server": "127.0.0.1"
		}
	]
}

```

#### Запуск приложения (Windows):

```
cd examples
cd api_import_receipts
..\..\venv\scripts\python.exe main.py
```

#### Обновление проекта из Git (Windows):

```
cd /opt/elq
git pull
venv/bin/python3 -m pip install --upgrade pip
venv/bin/pip install -r requirements.txt
venv/bin/python3 manage.py migrate
venv/bin/python3 manage.py runserver
```

#### Запуск приложения (Ubuntu):

```
cd examples
cd api_import_receipts
../../venv/bin/python3 examples/api_import_receipts/main.py 
```

#### Обновление проекта из Git (Ubuntu):

```
cd /opt/elq
git pull
venv\scripts\python.exe -m pip install --upgrade pip
venv\scripts\pip install -r requirements.txt
venv\scripts\python.exe manage.py migrate
venv\scripts\python.exe manage.py runserver
```
