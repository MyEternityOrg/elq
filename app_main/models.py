import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    """
        Отдел
        guid : Идентификатор отдела.
        name : Наименование отдела.
        create_date_time : Дата/время создания записи.
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД подразделения', editable=False)
    name = models.CharField(null=False, max_length=128, verbose_name='Название отдела', unique=True, db_column='name')
    create_date_time = models.DateTimeField(auto_now_add=True, editable=False,
                                            verbose_name='Дата заведения отдела', db_column='dts')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'department'
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Ware(models.Model):
    """
        Товар
        guid : Идентификатор товара.
        code : Локальный код товара.
        full_name : Наименование товара (полное).
        short_name : Наименование товара (краткое).
        department_guid : Отдел, где производится товар.
        create_date_time : Дата/время создания записи.
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД товара', editable=False)
    code = models.CharField(null=False, max_length=16, verbose_name='Локальный код товара', unique=True,
                            db_column='code')
    full_name = models.CharField(null=False, max_length=128, verbose_name='Название товара (полное)',
                                 db_column='f_name')
    short_name = models.CharField(null=False, max_length=64, verbose_name='Название товара (сокращенное)',
                                  db_column='s_name')
    department_guid = models.ForeignKey(Department, null=False, on_delete=models.CASCADE,
                                        verbose_name='Отдел производства товара', db_column='department_guid')
    create_date_time = models.DateTimeField(auto_now_add=True, editable=False,
                                            verbose_name='Дата заведения товара', db_column='dts')

    def __str__(self):
        return f'{self.code} {self.short_name} - {self.department_guid.name}'

    class Meta:
        db_table = 'ware'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Status(models.Model):
    """
        Статус
        id : Идентификатор статуса.
        name : Наименование статуса.
        finished : Является окончательным.
    """
    id = models.IntegerField(primary_key=True, db_column='id', verbose_name='ИД статуса', editable=False)
    name = models.CharField(null=False, max_length=64, verbose_name='Название статуса', unique=True, db_column='name')
    finished = models.BooleanField(default=False, verbose_name='Конечный статус', db_column='finished')
    show = models.BooleanField(default=True, verbose_name='Отображение статуса', db_column='show')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'status'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class StatusFlow(models.Model):
    """
        Очередность статусов
        guid : Идентификатор записи.
        current_status : Текущий статус.
        next_status : Следующий возможный статус.
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД записи', editable=False)
    current_status_guid = models.ForeignKey(Status, db_column='current_status_guid', verbose_name='Текущий статус',
                                            related_name='current_status',
                                            on_delete=models.DO_NOTHING)
    next_status_guid = models.ForeignKey(Status, db_column='next_status_guid', verbose_name='Следующий статус',
                                         related_name='next_status',
                                         on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.current_status_guid.name} -> {self.next_status_guid.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['current_status_guid', 'next_status_guid'],
                                    name="%(app_label)s_%(class)s_unique"),
        ]
        db_table = 'status_flow'
        verbose_name = 'Смена статуса'
        verbose_name_plural = 'Смены статусов'


class Document(models.Model):
    """
        Документ
        guid : Идентификатор документа.
        number : Номер документа.
        status : Статус документа.
        create_date : Дата создания документа.
        create_time : Время создания документа.
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД документа', editable=False)
    number = models.IntegerField(default=0, verbose_name='Номер заказа', db_index=True, db_column='number')
    status_guid = models.ForeignKey(Status, verbose_name='Статус заказа', on_delete=models.CASCADE,
                                    db_column='status_guid')
    create_date = models.DateField(auto_now_add=True, editable=False,
                                   verbose_name='Дата документа', db_index=True, db_column='create_date')
    create_time = models.TimeField(auto_now_add=True, editable=False,
                                   verbose_name='Время документа', db_index=True, db_column='create_time')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['number', 'create_date'], name="%(app_label)s_%(class)s_unique"),
        ]
        ordering = ['create_date', 'number']
        db_table = 'document'
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class DocumentWare(models.Model):
    """
        Состав документа
        guid : Идентификатор строки.
        document_guid :Идентификатор документа.
        ware_guid : Идентификатор товара.
        ware_count : Количество товара.
        status : Статус записи.
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД товара документа', editable=False)
    document_guid = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='ИД документа',
                                      db_column='document_guid')
    ware_guid = models.ForeignKey(Ware, on_delete=models.CASCADE, verbose_name='ИД товара', db_column='ware_guid')
    ware_count = models.IntegerField(default=1, verbose_name='Количество', db_column='cnt')
    status_guid = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус записи',
                                    db_column='status_guid')

    class Meta:
        db_table = 'document_ware'
        verbose_name = 'Состав документа'
        verbose_name_plural = 'Состав документов'


class DocumentHistory(models.Model):
    """
        История состава заказа
        guid : Идентификатор записи.
        document_ware_guid : Идентификатор строки ТЧ состава.
        status : Статус.
        create_date_time : Дата/время изменения.
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД записи', editable=False)
    document_ware_guid = models.ForeignKey(DocumentWare, on_delete=models.CASCADE, verbose_name='ИД записи документа',
                                           db_column='document_ware_guid')
    status_guid = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус', db_column='status_guid')
    create_date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_column='dts')

    class Meta:
        db_table = 'document_history'
        verbose_name = 'История документа'
        verbose_name_plural = 'История документов'
