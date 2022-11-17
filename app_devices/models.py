import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Count
from django.utils.timezone import now


class Printer(models.Model):
    """
        Сетевой принтер

        guid : Идентификатор.

        name : Наименование.

        ip_address : Адрес устройства в сети.

    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
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
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
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
        Хранится последний номер чека, который был получен к указанной кассы в разрезе даты.

        guid : Ключ записи.

        cash_id : Номер кассы.

        check_id : Номер чека.

        check_date: Дата смены чека.

    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД чека', editable=False)
    cash_guid = models.ForeignKey(Cash, on_delete=models.CASCADE, verbose_name='Номер кассы', db_column='cash_guid')
    check_id = models.IntegerField(default=1, null=False, verbose_name='Номер чека', db_column='check_id')
    check_date = models.DateField(default=now, verbose_name='Дата чека', db_column='check_dts', null=False)

    @staticmethod
    def register_cash_check(i_cash_id: int, i_check_id: int, i_check_date: datetime = now):
        """
        Регистрирует данные кассового чека, для быстрого ответа - нужна ли запись чека в документ или нет.

        :param i_cash_id: Идентификатор, номер кассы.
        :param i_check_id:  Номер чека.
        :param i_check_date: Дата чека.
        :return: bool:register result, str:message, guid:cash_guid
        """
        cash_guid = Cash.objects.filter(cash_number=i_cash_id).first()
        if cash_guid is None:
            return False, f'Invalid cash number, registered numbers are:' \
                          f' {[c.cash_number for c in Cash.objects.all()]}', None
        imported_check = ImportedChecks.objects.filter(cash_guid=cash_guid,
                                                       check_date=i_check_date).first()
        if imported_check is not None:
            if imported_check.check_id >= i_check_id:
                return False, f'Already have receipt with number {imported_check.check_id}' \
                              f' for cash {i_cash_id} ' \
                              f'in {i_check_date}', None
            else:
                imported_check.check_id = i_check_id
                imported_check.save()
                return True, 'Ok', cash_guid
        else:
            ImportedChecks.objects.create(cash_guid=cash_guid, check_id=i_check_id,
                                          check_date=i_check_date)
            return True, 'Ok', cash_guid

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cash_guid', 'check_id', 'check_date'],
                                    name="%(app_label)s_%(class)s_unique"),
        ]
        db_table = 'import_checks'
        verbose_name = 'Чек ККТ'
        verbose_name_plural = 'Чеки ККТ'
