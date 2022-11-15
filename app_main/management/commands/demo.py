import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_main.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        Document.objects.all().delete()
        wares = [w.guid for w in Ware.objects.all()]
        for i in range(1, 31):
            doc = Document.create_document()
            for k in range(1, 3):
                DocumentWare.add_ware(doc.guid, random.choice(wares), k)
