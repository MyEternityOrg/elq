# Generated by Django 4.1.3 on 2022-11-14 15:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.UUID('fe33f3b6-ed02-42c4-9586-cab38156320a'),
                                          editable=False, max_length=64, primary_key=True, serialize=False,
                                          verbose_name='ИД устройства')),
                ('name',
                 models.CharField(default='Нет названия', max_length=128, verbose_name='Наименование устройства')),
                ('ip_address', models.GenericIPAddressField(default='127.0.0.1', verbose_name='IP адрес устройства')),
            ],
            options={
                'verbose_name': 'Принтер',
                'verbose_name_plural': 'Принтеры',
                'db_table': 'printer',
            },
        ),
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.UUID('d7b6d71b-b215-40c8-b48e-70465db6959b'),
                                          editable=False, max_length=64, primary_key=True, serialize=False,
                                          verbose_name='ИД устройства')),
                ('name', models.CharField(db_column='name', default='Нет названия', max_length=128,
                                          verbose_name='Наименование устройства')),
                ('ip_address',
                 models.GenericIPAddressField(db_column='ip', default='127.0.0.1', verbose_name='IP адрес кассы')),
                ('pg_login', models.CharField(db_column='sql_login', max_length=64, verbose_name='Логин SQL')),
                ('pg_password', models.CharField(db_column='sql_passw', max_length=64, verbose_name='Пароль SQL')),
                ('pg_db_name', models.CharField(db_column='sql_db', max_length=64, verbose_name='Наименование БД')),
                ('request_interval', models.IntegerField(db_column='request_interval', default=2000,
                                                         verbose_name='Интервал опроса кассы, м/сек')),
                ('printer_guid',
                 models.ForeignKey(db_column='printer_guid', null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='app_devices.printer', verbose_name='Принтер')),
            ],
            options={
                'verbose_name': 'Касса',
                'verbose_name_plural': 'Кассы',
                'db_table': 'cash',
            },
        ),
    ]
