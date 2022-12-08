from django.contrib import admin
from .models import *

admin.site.register(Status)
admin.site.register(StatusFlow)
admin.site.register(Department)
admin.site.register(Ware)
admin.site.register(Document)
admin.site.register(DocumentWare)