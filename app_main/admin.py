from django.contrib import admin
from .models import *


class DocumetLine(admin.StackedInline):
    model = DocumentWare
    extra = 0


class DocWare(admin.ModelAdmin):
    inlines = [DocumetLine]


admin.site.register(Status)
admin.site.register(StatusFlow)
admin.site.register(Department)
admin.site.register(Document, DocWare)
admin.site.register(Ware)
