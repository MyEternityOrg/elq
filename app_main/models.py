import datetime
import uuid

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now

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
        indexes = [models.Index(fields=['name'])]
        db_table = 'department'
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ['name']


class Ware(models.Model):
    """
        Товар

        guid : Идентификатор товара.

        code : Локальный код товара.

        full_name : Наименование товара (полное).

        short_name : Наименование товара (краткое).

        department_guid : Отдел, где производится товар.

        create_date_time : Дата/время создания записи.

        catch_quantity : Из чеков будет отбираться только тот товар, количество которого больше или равно заданному.
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
    catch_quantity = models.FloatField(default=1, null=False, verbose_name='Минимальный порог', db_column='catch_qty')

    def __str__(self):
        return f'{self.code} {self.short_name} - {self.department_guid.name}'

    class Meta:
        indexes = [models.Index(fields=['code'])]
        db_table = 'ware'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['code']


class Status(models.Model):
    """
        Статус

        id : Идентификатор статуса.

        name : Наименование статуса.

        finished : Является окончательным.

        show : Отображать на экране.

        create_date_time : Дата/время создания статуса.
    """
    id = models.IntegerField(primary_key=True, db_column='id', verbose_name='ИД статуса', editable=False)
    name = models.CharField(null=False, max_length=64, verbose_name='Название статуса', unique=True, db_column='name')
    finished = models.BooleanField(default=False, verbose_name='Конечный статус', db_column='finished')
    show = models.BooleanField(default=True, verbose_name='Отображение статуса', db_column='show')
    create_date_time = models.DateTimeField(auto_now_add=True, editable=False,
                                            verbose_name='Дата записи', db_column='dts')
    color = models.CharField(default='gray', max_length=32, verbose_name='Цвет элемента')
    icon = models.CharField(default='bi bi-bag', max_length=64, verbose_name='Иконка элемента')

    @staticmethod
    def get_initial_status():
        """
        Получает начальный статус системы.
        
        :return: Статус, первый, который не является конечным и отображается на dashboard
        """
        return Status.objects.filter(finished=False, show=True).order_by('id').first()

    @staticmethod
    def get_dashboard_statuses():
        return [s.id for s in Status.objects.filter(finished=False, show=True).order_by('id')]

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['id']
        db_table = 'status'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class StatusFlow(models.Model):
    """
        Очередность статусов

        guid : Идентификатор записи.

        current_status : Текущий статус.

        next_status : Следующий возможный статус.

        create_date_time : Дата/время заведения связи.

    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД записи', editable=False)
    current_status_id = models.ForeignKey(Status, db_column='current_status_id', verbose_name='Текущий статус',
                                          related_name='current_status',
                                          on_delete=models.CASCADE)
    next_status_id = models.ForeignKey(Status, db_column='next_status_id', verbose_name='Следующий статус',
                                       related_name='next_status',
                                       on_delete=models.CASCADE)
    create_date_time = models.DateTimeField(auto_now_add=True, editable=False,
                                            verbose_name='Дата записи', db_column='dts')

    def __str__(self):
        return f'{self.current_status_id.name} -> {self.next_status_id.name}'

    class Meta:
        indexes = [models.Index(fields=['current_status_id', 'next_status_id'])]
        constraints = [
            models.UniqueConstraint(fields=['current_status_id', 'next_status_id'],
                                    name="%(app_label)s_%(class)s_unique"),
        ]
        ordering = ['current_status_id', 'next_status_id']
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
    status_id = models.ForeignKey(Status, verbose_name='Статус заказа', on_delete=models.CASCADE,
                                  db_column='status_id')
    create_date = models.DateField(auto_now_add=False, editable=False, default=now,
                                   verbose_name='Дата документа', db_index=True, db_column='create_date')
    create_time = models.TimeField(auto_now_add=True, editable=False,
                                   verbose_name='Время документа', db_index=True, db_column='create_time')

    def __str__(self):
        return f'{self.number}'

    @staticmethod
    def create_document(dts: datetime.date = None):
        """
        Создает электронной очереди новый документ для заполнения товарами.

        :param dts: Дата в которой надо создать документ

        :return: Созданный документ
        """
        if dts is None:
            dts = datetime.date.today()
        doc = Document.objects.filter(create_date=dts).order_by('create_time').last()
        if doc:
            return Document.objects.create(create_date=dts, number=doc.number + 1,
                                           status_id=Status.get_initial_status())
        else:
            return Document.objects.create(create_date=dts, number=1,
                                           status_id=Status.get_initial_status())

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

        status_guid : Статус записи.
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД товара документа', editable=False)
    document_guid = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='ИД документа',
                                      db_column='document_guid')
    ware_guid = models.ForeignKey(Ware, on_delete=models.CASCADE, verbose_name='ИД товара', db_column='ware_guid')
    ware_count = models.IntegerField(default=1, verbose_name='Количество', db_column='cnt')
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус записи',
                                  db_column='status_id')
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='ИД Пользователя')

    def __str__(self):
        return f'({self.document_guid.create_date}) {self.document_guid.number}: {self.ware_guid.short_name} ' \
               f'{self.ware_count}'

    @staticmethod
    def add_ware(document_guid, ware_guid, ware_count, user_id=1):
        """
        Добавить строчку товара в документ

        :param document_guid: Идентификатор документа.
        :param ware_guid:  Идентификатор товара.
        :param ware_count: Количество товара (будет увеличено на заданное количество, если существует).
        :param user_id: Пользователь-редактор.
        :return: Строка документа или None
        """
        ware = Ware.objects.filter(guid=ware_guid).first()
        user = User.objects.filter(id=user_id).first()
        if ware is not None:
            doc = Document.objects.filter(guid=document_guid).first()
            line = DocumentWare.objects.filter(document_guid=doc.guid, ware_guid=ware.guid).first()
            if line is None:
                line = DocumentWare.objects.create(document_guid=doc, ware_guid=ware, ware_count=ware_count,
                                                   status_id=Status.get_initial_status(), user_id=user)
            else:
                line.ware_count = line.ware_count + ware_count
                line.user_id = user
                line.save()
            return line
        return None

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

        user_id : Пользователь
    """
    guid = models.CharField(primary_key=True, db_column='guid', default=uuid.uuid4, max_length=64,
                            verbose_name='ИД записи', editable=False)
    document_ware_guid = models.ForeignKey(DocumentWare, on_delete=models.CASCADE, verbose_name='ИД записи документа',
                                           db_column='document_ware_guid')
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус', db_column='status_id')
    create_date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_column='dts')
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='ИД Пользователя')

    @receiver(post_save, sender=DocumentWare)
    def create_article(sender, instance, created, **kwargs):
        DocumentHistory.objects.create(document_ware_guid=instance, status_id=instance.status_id,
                                       user_id=instance.user_id)

    class Meta:
        db_table = 'document_history'
        verbose_name = 'История документа'
        verbose_name_plural = 'История документов'
