import datetime
import json
import os
import time
from contextlib import closing

import psycopg2
import requests
from psycopg2.extras import DictCursor


def read_data(sql: str = '', sql_server: str = '127.0.0.1', sql_database: str = 'cash',
              sql_login: str = 'postgres', sql_password: str = 'postgres'):
    os.environ['PGOPTIONS'] = '-c statement_timeout=300000'
    if sql == '':
        with open('main.sql', encoding='utf-8') as f:
            sql = f.read()

    with closing(psycopg2.connect(dbname=sql_database, user=sql_login, password=sql_password, host=sql_server)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql)
            for row in cursor:
                yield row


def prepared_request(cash=None):
    if cash is None:
        cash = {}
    result_data = {}
    for res in read_data(**cash):
        if result_data.get(res[1], None) is None:
            result_data[res[1]] = {'cash_id': res[0], 'check_id': res[1], 'check_date': res[2], 'wares': []}
        result_data[res[1]]['wares'].append({'ware_code': res[3], 'ware_count': res[4]})

    for el in result_data.values():
        yield json.dumps(el)


def proceed_data(system_settings=None):
    if system_settings is None:
        system_settings = {}
    for c in system_settings.get('cashes'):
        for k in prepared_request(c):
            r = requests.session()
            h = {'key': f'{system_settings.get("api_key", "secret_key_here")}'}
            r.headers.update(h)
            r.trust_env = False
            r = requests.post(f'{system_settings.get("api", "http://127.0.0.1/devices/import_receipt")}', headers=h,
                              data=k)
            reply = r.json()
            if dict(reply).get('doc_number', 0) > 0:
                print(
                    f'[{datetime.datetime.now()}] Registered receipt: '
                    f'{dict(reply).get("doc_number")} for CashID: '
                    f'{json.loads(k).get("cash_id")}')


if __name__ == "__main__":
    with open('main.json', encoding='UTF8') as f:
        settings = json.loads(f.read())
    while True:
        try:
            proceed_data(settings)
            time.sleep(settings.get("timer", 3))
        except Exception as E:
            print(f'Fail: {E}')
