import datetime
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_main.models import *
from app_main.management.commands.init import get_status


class Command(BaseCommand):
    def handle(self, *args, **options):
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

        Document.objects.all().delete()
        d = datetime.date.today().day
        m = datetime.date.today().month
        y = datetime.date.today().year
        if d > 3:
            d_arr = [d - 2, d - 1, d]
        elif d == 2:
            d_arr = [d-1, d]
        else:
            d_arr = [d]
        wares = [w.guid for w in Ware.objects.all()]
        for i in range(1, 101):
            doc = Document.create_document(datetime.date(y, m, random.choice(d_arr)))
            for k in range(1, 3):
                DocumentWare.add_ware(doc.guid, random.choice(wares), k)
            doc.status_id = get_status(random.choice([1, 2, 3, 4]))
            doc.save()
