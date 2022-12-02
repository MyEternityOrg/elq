import datetime
import uuid

from app_devices.printer.printer import print_receipt
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from app_main.models import Ware, DocumentWare, Document, Status
from elq.settings import CALC_PRINT_TICKETS


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

    @staticmethod
    def print_document(printer, document_number: int, dts: datetime.date = now, doc_count: int = 0):
        if printer is not None:
            if not CALC_PRINT_TICKETS:
                doc_count = 1
            else:
                doc_count += 1
            print_receipt(printer.name, str(document_number), doc_count,
                          datetime.datetime.today().strftime('%Y-%m-%d %H:%M'))

    class Meta:
        indexes = [models.Index(fields=['name'])]
        db_table = 'printer'
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'
        ordering = ['name']


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
    pg_login = models.CharField(default='postgres', max_length=64, verbose_name='Логин SQL', db_column='sql_login')
    pg_password = models.CharField(default='postgres', max_length=64, verbose_name='Пароль SQL', db_column='sql_passw')
    pg_db_name = models.CharField(default='cash', max_length=64, verbose_name='Наименование БД', db_column='sql_db')
    request_interval = models.IntegerField(default=2000, verbose_name='Интервал опроса кассы, м/сек',
                                           db_column='request_interval')

    def __str__(self):
        return f'{self.name} ({self.ip_address})'

    class Meta:
        indexes = [models.Index(fields=['cash_number'])]
        db_table = 'cash'
        verbose_name = 'Касса'
        verbose_name_plural = 'Кассы'
        ordering = ['cash_number']


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
    shift_id = models.IntegerField(default=1, null=False, verbose_name='Номер смены', db_column='shift_id')
    check_date = models.DateField(default=now, verbose_name='Дата чека', db_column='check_dts', null=False)

    @staticmethod
    def check_ware(ware_code: str = None, ware_count: int = None):
        ware = Ware.objects.filter(code=ware_code, catch_quantity__lte=ware_count).first()
        if ware:
            return ware.guid, ware_count
        else:
            return None, None

    @staticmethod
    def process_check_data(json_array=None, dts: datetime.date = now):
        wares_list = []
        depart_count = []
        try:
            if type(json_array) is list:
                for k in json_array:
                    if type(k) is dict:
                        ware_guid, ware_cnt = ImportedChecks.check_ware(**k)
                        if ware_guid is not None:
                            wares_list.append([ware_guid, ware_cnt])
                    else:
                        return False, 'Invalid json structure', -1
                if len(wares_list) > 0:
                    document = Document.create_document(dts)
                    if document is not None:
                        for k in wares_list:
                            depart_count.append(Ware.objects.get(guid=k[0]).department_guid.guid)
                            DocumentWare.add_ware(document.guid, k[0], k[1])
                        return True, '', document.number, len(set(depart_count))
                    else:
                        return False, 'Error registering document', -1, 0
                else:
                    return False, 'Nothing to register', 0, 0
            else:
                return False, 'Invalid json structure', -1, 0
        except Exception as E:
            return False, f'{E}', -1

    @staticmethod
    def register_cash_check(i_cash_id: int, i_shift_id: int, i_check_id: int, i_check_date: datetime.date = now,
                            json_array=None):
        """
        Регистрирует данные кассового чека, для быстрого ответа - нужна ли запись чека в документ или нет.

        :param i_cash_id: Идентификатор, номер кассы.
        :param i_check_id:  Номер чека.
        :param i_check_date: Дата чека.
        :param json_array: Массив данных чека.
        :return: bool:register result, str:message
        """
        if json_array is None:
            json_array = []
        doc_number = -1
        doc_msg = ''
        doc_state = False
        doc_printer = None
        doc_count = 0

        cash_guid = Cash.objects.filter(cash_number=i_cash_id).first()
        if cash_guid is None:
            return False, f'Invalid cash number, registered numbers are:' \
                          f' {[c.cash_number for c in Cash.objects.all()]}', doc_number, None, 0
        doc_printer = cash_guid.printer_guid
        imported_check = ImportedChecks.objects.filter(cash_guid=cash_guid,
                                                       check_date=i_check_date, shift_id=i_shift_id).first()
        if imported_check is not None:
            if imported_check.check_id >= i_check_id:
                return False, f'Already have receipt with number {imported_check.check_id}' \
                              f' for cash {i_cash_id} ' \
                              f'in {i_check_date}', doc_number, doc_printer, 0
            else:
                doc_state, doc_msg, doc_number, doc_count = ImportedChecks.process_check_data(json_array, i_check_date)
                if doc_state:
                    imported_check.check_id = i_check_id
                    imported_check.save()
                    return True, '', doc_number, doc_printer, doc_count
                else:
                    return doc_state, doc_msg, doc_number, doc_printer, doc_count
        else:
            doc_state, doc_msg, doc_number, doc_count = ImportedChecks.process_check_data(json_array, i_check_date)
            if doc_state:
                ImportedChecks.objects.create(cash_guid=cash_guid, check_id=i_check_id, shift_id=i_shift_id,
                                              check_date=i_check_date)
                return True, '', doc_number, doc_printer, doc_count
            else:
                return doc_state, doc_msg, doc_number, doc_printer, doc_count

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cash_guid', 'check_id', 'shift_id', 'check_date'],
                                    name="%(app_label)s_%(class)s_unique"),
        ]
        db_table = 'import_checks'
        verbose_name = 'Чек ККТ'
        verbose_name_plural = 'Чеки ККТ'
