# Generated by Django 4.1.3 on 2022-11-28 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0003_status_icon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['name'], 'verbose_name': 'Отдел', 'verbose_name_plural': 'Отделы'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['id'], 'verbose_name': 'Статус', 'verbose_name_plural': 'Статусы'},
        ),
        migrations.AlterModelOptions(
            name='statusflow',
            options={'ordering': ['current_status_id', 'next_status_id'], 'verbose_name': 'Смена статуса', 'verbose_name_plural': 'Смены статусов'},
        ),
        migrations.AlterModelOptions(
            name='ware',
            options={'ordering': ['code'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['name'], name='department_name_9f4150_idx'),
        ),
        migrations.AddIndex(
            model_name='statusflow',
            index=models.Index(fields=['current_status_id', 'next_status_id'], name='status_flow_current_5d96e1_idx'),
        ),
        migrations.AddIndex(
            model_name='ware',
            index=models.Index(fields=['code'], name='ware_code_6e4b2a_idx'),
        ),
    ]