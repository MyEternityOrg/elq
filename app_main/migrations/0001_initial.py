# Generated by Django 4.1.3 on 2022-11-16 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='ИД подразделения')),
                ('name', models.CharField(db_column='name', max_length=128, unique=True, verbose_name='Название отдела')),
                ('create_date_time', models.DateTimeField(auto_now_add=True, db_column='dts', verbose_name='Дата заведения отдела')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='ИД документа')),
                ('number', models.IntegerField(db_column='number', db_index=True, default=0, verbose_name='Номер заказа')),
                ('create_date', models.DateField(db_column='create_date', db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата документа')),
                ('create_time', models.TimeField(auto_now_add=True, db_column='create_time', db_index=True, verbose_name='Время документа')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'db_table': 'document',
                'ordering': ['create_date', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.IntegerField(db_column='id', editable=False, primary_key=True, serialize=False, verbose_name='ИД статуса')),
                ('name', models.CharField(db_column='name', max_length=64, unique=True, verbose_name='Название статуса')),
                ('finished', models.BooleanField(db_column='finished', default=False, verbose_name='Конечный статус')),
                ('show', models.BooleanField(db_column='show', default=True, verbose_name='Отображение статуса')),
                ('create_date_time', models.DateTimeField(auto_now_add=True, db_column='dts', verbose_name='Дата записи')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
                'db_table': 'status',
            },
        ),
        migrations.CreateModel(
            name='Ware',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='ИД товара')),
                ('code', models.CharField(db_column='code', max_length=16, unique=True, verbose_name='Локальный код товара')),
                ('full_name', models.CharField(db_column='f_name', max_length=128, verbose_name='Название товара (полное)')),
                ('short_name', models.CharField(db_column='s_name', max_length=64, verbose_name='Название товара (сокращенное)')),
                ('create_date_time', models.DateTimeField(auto_now_add=True, db_column='dts', verbose_name='Дата заведения товара')),
                ('catch_quantity', models.FloatField(db_column='catch_qty', default=1, verbose_name='Минимальный порог')),
                ('department_guid', models.ForeignKey(db_column='department_guid', on_delete=django.db.models.deletion.CASCADE, to='app_main.department', verbose_name='Отдел производства товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'ware',
            },
        ),
        migrations.CreateModel(
            name='StatusFlow',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='ИД записи')),
                ('create_date_time', models.DateTimeField(auto_now_add=True, db_column='dts', verbose_name='Дата записи')),
                ('current_status_id', models.ForeignKey(db_column='current_status_id', on_delete=django.db.models.deletion.CASCADE, related_name='current_status', to='app_main.status', verbose_name='Текущий статус')),
                ('next_status_id', models.ForeignKey(db_column='next_status_id', on_delete=django.db.models.deletion.CASCADE, related_name='next_status', to='app_main.status', verbose_name='Следующий статус')),
            ],
            options={
                'verbose_name': 'Смена статуса',
                'verbose_name_plural': 'Смены статусов',
                'db_table': 'status_flow',
            },
        ),
        migrations.CreateModel(
            name='DocumentWare',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='ИД товара документа')),
                ('ware_count', models.IntegerField(db_column='cnt', default=1, verbose_name='Количество')),
                ('document_guid', models.ForeignKey(db_column='document_guid', on_delete=django.db.models.deletion.CASCADE, to='app_main.document', verbose_name='ИД документа')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.CASCADE, to='app_main.status', verbose_name='Статус записи')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='ИД Пользователя')),
                ('ware_guid', models.ForeignKey(db_column='ware_guid', on_delete=django.db.models.deletion.CASCADE, to='app_main.ware', verbose_name='ИД товара')),
            ],
            options={
                'verbose_name': 'Состав документа',
                'verbose_name_plural': 'Состав документов',
                'db_table': 'document_ware',
            },
        ),
        migrations.CreateModel(
            name='DocumentHistory',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='ИД записи')),
                ('create_date_time', models.DateTimeField(auto_now_add=True, db_column='dts', verbose_name='Дата создания')),
                ('document_ware_guid', models.ForeignKey(db_column='document_ware_guid', on_delete=django.db.models.deletion.CASCADE, to='app_main.documentware', verbose_name='ИД записи документа')),
                ('status_id', models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.CASCADE, to='app_main.status', verbose_name='Статус')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='ИД Пользователя')),
            ],
            options={
                'verbose_name': 'История документа',
                'verbose_name_plural': 'История документов',
                'db_table': 'document_history',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='status_id',
            field=models.ForeignKey(db_column='status_id', on_delete=django.db.models.deletion.CASCADE, to='app_main.status', verbose_name='Статус заказа'),
        ),
        migrations.AddConstraint(
            model_name='statusflow',
            constraint=models.UniqueConstraint(fields=('current_status_id', 'next_status_id'), name='app_main_statusflow_unique'),
        ),
        migrations.AddConstraint(
            model_name='document',
            constraint=models.UniqueConstraint(fields=('number', 'create_date'), name='app_main_document_unique'),
        ),
    ]
