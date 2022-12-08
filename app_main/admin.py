from django.contrib import admin
from .models import *


class DocumentLine(admin.StackedInline):
    model = DocumentWare
    fields = ['ware_guid', 'ware_count']
    extra = 0


class DocWare(admin.ModelAdmin):
    inlines = [DocumentLine]


admin.site.register(Status)
admin.site.register(StatusFlow)
admin.site.register(Department)
admin.site.register(Document, DocWare)
admin.site.register(Ware)
