# 1. Общие положения
## 1.1. Описание.
Система регистрации чеков в электронной очереди производства, состоит из двух основных компонентов:
- `Django` - приложение самой электронной очереди и печати номеров заказов
- Приложение сборщик данных по продажам из касс `Set Retail 10 (Crystal)`
- Каждый компонент запускается в своем `Docker` контейнере. Названия контейнеров `elq` и `api_import` соответственно.
- Приложение доступно по следующим портам:
    - `8000` - веб-интерфейс электронной очереди
    - `631` - настройка `CUPS`
## 1.2. Требования к размещению и функционированию
- Если настройка и установка происходит из сети магазина, то на период установки **необходимо отключить Firewall**, это можно сделать через бота управления `mikrotik` магазина. После завершения настройки, `Firewall` нужно включить.
- Для работы приложения `Электронная очередь` требуется `Docker`, версия не ниже `20.10.17`, `Linux` или `Windows`.
- Все настройки `Django` передаются через переменные окружения, в файле `.env`.
- Настройки `Приложение сборщик данных` в файле `main.json`. 
- Для печати номера заказов должен быть настроен принтер `SAM4s ELLIX50`. Принтер должен быть доступен через сетевое соединение.
- Подробное описание файла настроек `.env` и `main.json` и настройка `CUPS`  в разделе [2.3. Установка и настройка приложения]().
# 2. Установка и настройка
## 2.1. Установка `Docker` на примере Ubuntu 20.04
* Обновляем индексы apt
```bash
 sudo apt-get update

 sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```
* Добавляем GPG ключ `Docker`
```bash
 sudo mkdir -p /etc/apt/keyrings

 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
* Подключаем репозиторий `Docker`
```bash
 echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  ```
* Устанавливаем `Docker Engine`
```bash
 sudo apt-get update

 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
 ```
* Проверяем версию
```bash
docker --version
```
## 2.2. Настройка запуска `Docker` без `sudo`
* Создаем группу `docker`
```bash
sudo groupadd docker
```
* Добавляем текущего пользователя `$USER` в группу `docker`
```bash
sudo usermod -aG docker $USER
```
* Применяем изменения
```bash
newgrp docker
```
* Проверяем запуск без `sudo`
```bash
docker run hello-world
```
## 2.3. Установка и настройка приложения

### 2.3.1. Запуск контейнеров
- Клонируем репозиторий приложения

```bash
git clone https://github.com/MyEternityOrg/elq
```
- Переходим в директорию проекта
```bash
cd elq
```
- Настройки `Django` приложения находятся в файл `.env`. Переименовываем файл с примерами настроек в `.env`
```bash
mv .env.sample .env
```
- Вносим изменения, если необходимо. Важным является ключ `API_KEY` к интерфейсу получения кассовых чеков, его необходимо сохранить и указать в настройках `Приложения сборщик данных` в файле `main.json`. 

```bash
nano .env
```
```
API_KEY = 'secret_key_here'
SQL_ENGINE = 'django.db.backends.sqlite3'
SQL_DB_NAME = './elq.sqlite3'
SQL_DB_USER = 'user'
SQL_DB_PASSWORD = 'pass'
SQL_DB_HOST = '.'
SQL_DB_PORT = 1433
SQL_OPTIONS = '{}'
```
- Настраиваем `Приложения сборщик данных`. Переименовываем файл с примерами настроек в `main.json`
```bash
mv ./api_import_receipts/main.json.sample ./api_import_receipts/main.json
```
- Редактируем файл, нужно указать ключ `API_KEY` из файла `.env` и настроить ip адреса касс.
```bash
nano ./api_import_receipts/main.json
```

Пример настройки для `Магазина 116` :
```json
{
	"api": "http://elq:8000/devices/import_receipt/",
	"api_key": "secret_key_here",
	"timer": 3,
	"cashes": [
		{
			"sql_server": "10.1.16.11"
		},
		{
			"sql_server": "10.1.16.12"
		},
		{
			"sql_server": "10.1.16.13"
		},
		{
			"sql_server": "10.1.16.14"
		},
		{
			"sql_server": "10.1.16.15"
		}
	]
}
```
- Запускаем контейнеры
```bash
docker compose up -d
```
* Дожидаемся сбора образов и запуска. Проверяем, что контейнеры в статусе `up`
```bash
docker ps -a
```
* Если возникли проблемы, можно посмотреть лог

```bash
docker logs elq
```
```bash
docker logs api_import
```
### 2.3.2. Настройка `CUPS`
- Для печати талонов нужно настроить принтер в службе `CUPS`, она доступа по адресу. Логин/пароль `print`.
```
http://ip_сервера:631/
```
- Добавляем принтер с подключением через socket, в строке подключения указываем
```
socket://ip_принтера:6001
```
- Важно запомнить имя под которым добавляется принтер, например `ELLIX50`. Его затем нужно будет указать в веб интерфейсе `Django` приложения
- на этапе выбора модели нужно подгрузить `PPT` файл. Для модели `SAM4s ELLIX50` файл можно скачать по прямой ссылке [git](https://github.com/MyEternityOrg/elq/blob/master/SAM4s_GIANT100.ppd)
- Для проверки можно отправить тестовую страницу на печать
### 2.3.3. Настройка приложения
- Приложение доступно по ссылке. Логин/пароль магазина `shop 123`
```
http://ip_сервера:8000/
```
- В разделе администрирования настраиваются `Кассы` и `Принтеры`. **ВАЖНО**. Имя принтера нужно взять из раздела [2.3.2. Настройка `CUPS`]()

```
http://ip_сервера:8000/admin/
```
### 2.3.4. Внесение правок в файлы конфигурации
Если нужно внести изменения в файлы в уже развернутом приложении:
- для изменения файла `main.json`
```bash
cd elq
docker exec -it api_import /bin/sh
nano ./elq/api_import_receipts/main.json
```
- для изменения файла `.env`
```bash
cd elq
docker exec -it elq /bin/sh
nano ./elq/.env
```
после внесения правок, нужно отключиться от контейнера и выполнить перезапуск

```bash
exit
docker compose stop
docker compose up -d
```
### 2.3.5. Установка обновлений
Обновления устанавливаются автоматически из `github` при перезапуске контейнеров.

```bash
cd elq
docker compose stop
docker compose up -d
```
# 3. Интеграция
Интерфейс 
```
http://ip_сервера:8000/devices/import_receipt/
```
принимает входящие POST запросы и регистрирует чеки.
В заголовке запроса должен быть передан api_key, в теле запроса файл импорта чека.

Для ограничения доступа к post интерфейсу получения кассовых чеков можно задать свой собственный `api_key`, в файле `.env`

```
API_KEY = 'secret_key_here'
```

Пример, для `curl`:

```
curl -H "key:secret_key_here" --data "@receipt_1.json" http://127.0.0.1/devices/import_receipt/ > reply_1.json
```
## Пример файла импорта чека:

* `cash_id` - Номер кассы
* `shift_id` - Номер смены.
* `check_id` - Номер чека в смене.
* `check_date` - Дата чека.
* `wares` - Массив товаров (сгруппирован по товарам с суммой по количеству)
    * `ware_code` - Код товара в чеке.
    * `ware_count` - Количество товара в чеке.

```json
{
	"cash_id": 1,
	"shift_id": 1,
	"check_id": 1,
	"check_date": "2022-11-17",
	"wares": [
		{
			"ware_code": "48566",
			"ware_count": 4
		},
		{
			"ware_code": "51356",
			"ware_count": 1
		},
		{
			"ware_code": "72542",
			"ware_count": 1
		}
	]
}
```

## Файл ответа с информацией о номере очереди:

В случае успешной регистрации, система вернет номер очереди `doc_number>0`.

В случае ошибки - система вернет `doc_number=0` и описание ошибки.

В случае, когда действий не требуется (нечего регистрировать) система вернет `doc_number=-1` и сообщение.

Пример файла ответа:

```json
{"doc_number": -1, "error": "Already have receipt with number 1 for cash 1 in 2022-11-21"}
```
