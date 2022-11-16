import datetime
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_main.models import *
from app_main.management.commands.init import get_status


class Command(BaseCommand):
    def handle(self, *args, **options):
        Document.objects.all().delete()
        d = datetime.date.today().day
        d_arr = [d - 2, d - 1, d]
        wares = [w.guid for w in Ware.objects.all()]
        for i in range(1, 101):
            doc = Document.create_document(datetime.date(2022, 11, random.choice(d_arr)))
            for k in range(1, 3):
                DocumentWare.add_ware(doc.guid, random.choice(wares), k)
            doc.status_id = get_status(random.choice([1, 2, 3, 4]))
            doc.save()
