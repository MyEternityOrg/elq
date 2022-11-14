from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from app_main.models import *
from app_devices.models import *


def get_status(status_id: int):
    return Status.objects.get(id=status_id)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Initializing database...')

        print('Creating default users...')
        User.objects.all().delete()
        User.objects.create(id=1, username='root',
                            password='pbkdf2_sha256$390000$9g7tM3eD6Jx9qLyrf2aqVa$iuMWfgtEtchzjhSp+f25ehCikPzDm6Q1C0z24dDpZog=',
                            email='a.kovalenko@pokupochka.ru', is_staff=True, is_active=True, is_superuser=True)
        User.objects.create(id=2, username='shop',
                            password='pbkdf2_sha256$390000$7KYChLAKiOnRkiV7ozUGMz$mQ/ZUcfI3NU0+07RmdPwmKYKvn2pID5faYqTzOZ2tWg=',
                            email='shop@pokupochka.ru', is_staff=True, is_active=True, is_superuser=True)
        for i in range(1, 9):
            User.objects.create(id=i + 2, username=f'reserved_{i}', is_staff=True, is_active=True, is_superuser=True)

        print('Creating departments...')
        Department.objects.all().delete()
        Department.objects.create(guid='dd5637f2-a982-4de7-9962-54c7790f7787', name='Салаты')
        Department.objects.create(guid='0ca520d0-2be8-4336-9555-ab8411729862', name='Шаурма')
        Department.objects.create(guid='0d7aa2be-8b1c-4d1d-9003-0da8d0527693', name='Пиццерия')
        Department.objects.create(guid='55f6079a-ea34-4303-a531-5fc80d00a7c2', name='Вок')

        print('Creating statuses...')
        Status.objects.all().delete()
        Status.objects.create(id=1, name='Готовится', show=True, finished=False)
        Status.objects.create(id=2, name='Готов к выдаче', show=True, finished=False)
        Status.objects.create(id=3, name='Выдан', show=False, finished=True)
        Status.objects.create(id=4, name='Отменен', show=False, finished=True)

        print('Creating status flow rules...')
        StatusFlow.objects.all().delete()
        StatusFlow.objects.create(current_status_id=get_status(1), next_status_id=get_status(2))
        StatusFlow.objects.create(current_status_id=get_status(1), next_status_id=get_status(4))
        StatusFlow.objects.create(current_status_id=get_status(2), next_status_id=get_status(3))
        StatusFlow.objects.create(current_status_id=get_status(2), next_status_id=get_status(4))

        print('Creating demo devices...')
        Printer.objects.all().delete()
        Printer.objects.create(name='Принтер этикеток', ip_address='127.0.0.1')

        Cash.objects.all().delete()
        Cash.objects.create(name='Касса №1', ip_address='127.0.0.1', pg_db_name='set_operday', pg_login='set',
                            pg_password='set', printer_guid=Printer.objects.first())

        print('Creating demo wares...')
        Ware.objects.all().delete()
        Ware.objects.create(code=48566, full_name='Пицца ароматная, вкусная, с сыром маскароне',
                            short_name='Пицца 4 сыра',
                            department_guid=Department.objects.get(guid='0d7aa2be-8b1c-4d1d-9003-0da8d0527693'))
        Ware.objects.create(code=43221, full_name='Шаурма со свининой', short_name='Шаурма св',
                            department_guid=Department.objects.get(guid='0ca520d0-2be8-4336-9555-ab8411729862'))
        Ware.objects.create(code=51356, full_name='Вок острый, с пряным соусом', short_name='Вок остр. пр. соус',
                            department_guid=Department.objects.get(guid='55f6079a-ea34-4303-a531-5fc80d00a7c2'))
        Ware.objects.create(code=51358, full_name='Вок острый, с гречневой лапшой', short_name='Вок остр. греча',
                            department_guid=Department.objects.get(guid='55f6079a-ea34-4303-a531-5fc80d00a7c2'))
        Ware.objects.create(code=12356, full_name='Салат оливье, новогодний', short_name='Салат оливье',
                            department_guid=Department.objects.get(guid='dd5637f2-a982-4de7-9962-54c7790f7787'))
