from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from app_main.models import *
from app_devices.models import *
from elq.settings import *


def get_status(status_id: int):
    return Status.objects.get(id=status_id)


class Command(BaseCommand):
    def handle(self, *args, **options):

        print('Optimizing...')
        finished_state = [e.id for e in Status.objects.filter(finished=True)]
        clear_arr = Document.objects.filter(status_id__in=finished_state)
        total_docs = len(clear_arr)
        total_wares = 0
        total_history = 0
        for el in clear_arr:
            doc = Document.objects.get(guid=el.guid)
            wares = DocumentWare.objects.filter(document_guid=doc.guid)
            total_wares += len(wares)
            for ware in wares:
                total_history += len(DocumentHistory.objects.filter(document_ware_guid=ware.guid))
                DocumentHistory.objects.filter(document_ware_guid=ware.guid).delete()
                ware.delete()
            doc.delete()
        print(f'Optimization: Done, removed: {total_docs} docs, {total_wares} lines, {total_history} history records.')
