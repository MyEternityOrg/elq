# Generated by Django 4.1.3 on 2022-11-28 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_devices', '0003_remove_importedchecks_app_devices_importedchecks_unique_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cash',
            options={'ordering': ['cash_number'], 'verbose_name': 'Касса', 'verbose_name_plural': 'Кассы'},
        ),
        migrations.AlterModelOptions(
            name='printer',
            options={'ordering': ['name'], 'verbose_name': 'Принтер', 'verbose_name_plural': 'Принтеры'},
        ),
        migrations.AddIndex(
            model_name='cash',
            index=models.Index(fields=['cash_number'], name='cash_cash_id_1b4235_idx'),
        ),
        migrations.AddIndex(
            model_name='printer',
            index=models.Index(fields=['name'], name='printer_name_87bbe4_idx'),
        ),
    ]
