# Generated by Django 4.1.3 on 2022-12-06 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_devices', '0004_alter_cash_options_alter_printer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='pg_password',
            field=models.CharField(db_column='sql_pass', default='postgres', max_length=64, verbose_name='Пароль SQL'),
        ),
    ]
