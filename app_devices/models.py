import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Count


class Printer(models.Model):
    """
        Сетевой принтер

        guid : Идентификатор.

        name : Наименование.

        ip_address : Адрес устройства в сети.

    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4(), max_length=64,
                            verbose_name='ИД устройства', editable=False)
    name = models.CharField(max_length=128, default='Нет названия', verbose_name='Наименование устройства')
    ip_address = models.GenericIPAddressField(default='127.0.0.1', null=False, verbose_name='IP адрес устройства')

    def __str__(self):
        return f'{self.name} ({self.ip_address})'

    class Meta:
        db_table = 'printer'
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'


class Cash(models.Model):
    """
        Касса

        guid : Идентификатор.

        name : Наименование кассы.

        ip_address : Адрес устройства в сети.

        cash_printer : Принтер. Если задан, то касса печатает на нем полученные данные заказа.

        pg_login : Логин для postgre кассы.

        pg_password : Пароль для postgre кассы.

        pd_db_name : Имя БД postgre кассы.

        request_interval: Интервал опроса кассы в миллисекундах

    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4(), max_length=64,
                            verbose_name='ИД устройства', editable=False)
    cash_number = models.IntegerField(default=1, unique=True, null=False, verbose_name='Номер кассы',
                                      db_column='cash_id')
    name = models.CharField(max_length=128, default='Нет названия', verbose_name='Наименование устройства',
                            db_column='name')
    ip_address = models.GenericIPAddressField(default='127.0.0.1', null=False, verbose_name='IP адрес кассы',
                                              db_column='ip')
    printer_guid = models.ForeignKey(Printer, null=True, on_delete=models.CASCADE, verbose_name='Принтер',
                                     db_column='printer_guid')
    pg_login = models.CharField(max_length=64, verbose_name='Логин SQL', db_column='sql_login')
    pg_password = models.CharField(max_length=64, verbose_name='Пароль SQL', db_column='sql_passw')
    pg_db_name = models.CharField(max_length=64, verbose_name='Наименование БД', db_column='sql_db')
    request_interval = models.IntegerField(default=2000, verbose_name='Интервал опроса кассы, м/сек',
                                           db_column='request_interval')

    def __str__(self):
        return f'{self.name} ({self.ip_address})'

    class Meta:
        db_table = 'cash'
        verbose_name = 'Касса'
        verbose_name_plural = 'Кассы'


class ImportedChecks(models.Model):
    """
        Данные импортируемых чеков.

        cash_id : Номер кассы.

        check_id : Номер чека.

        check_date: Дата смены чека.

        ware_code : Код товара

        ware_count : Количество товара в чеке.

        create_date_time : Дата/время импорта

        processed : Признак обработки чека.
    """
    cash_id = models.IntegerField(default=1, null=False, verbose_name='Номер кассы', db_column='cash_id')
    check_id = models.IntegerField(default=1, null=False, verbose_name='Номер чека', db_column='check_id')
    check_date = models.DateField(auto_now_add=True, verbose_name='Дата чека', db_column='check_dts', null=False)
    ware_code = models.CharField(null=False, max_length=16, verbose_name='Локальный код товара', unique=True,
                                 db_column='code')
    ware_count = models.IntegerField(default=1, verbose_name='Количество', db_column='cnt')
    create_date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_column='dts')
    processed = models.BooleanField(default=False, null=False, verbose_name='Обработан', db_column='processed')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cash_id', 'check_id', 'check_date'],
                                    name="%(app_label)s_%(class)s_unique"),
        ]
        db_table = 'import_checks'
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
