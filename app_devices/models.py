import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Count


class ModelPrinterDevice(models.Model):
    """
        Сетевой принтер.

        guid : Идентификатор

        name : Наименование

        ip_address : Адрес устройства в сети
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4(), max_length=64,
                            verbose_name='ИД устройства')
    name = models.CharField(max_length=128, default='Нет названия', verbose_name='Наименование устройства')
    ip_address = models.GenericIPAddressField(default='127.0.0.1', null=False, verbose_name='IP адрес устройства')

    class Meta:
        db_table = 'printer'
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'


class ModelCash(models.Model):
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
                            verbose_name='ИД устройства')
    name = models.CharField(max_length=128, default='Нет названия', verbose_name='Наименование устройства')
    ip_address = models.GenericIPAddressField(default='127.0.0.1', null=False, verbose_name='IP адрес устройства')
    cash_printer = models.ForeignKey(ModelPrinterDevice, null=True, on_delete=models.CASCADE, verbose_name='Принтер')
    pg_login = models.CharField(max_length=64, verbose_name='Логин SQL')
    pg_password = models.CharField(max_length=64, verbose_name='Пароль SQL')
    pg_db_name = models.CharField(max_length=64, verbose_name='Наименование БД')
    request_interval = models.IntegerField(default=2000, verbose_name='Интервал опроса кассы, м/сек')

    class Meta:
        db_table = 'cash'
        verbose_name = 'Касса'
        verbose_name_plural = 'Кассы'

