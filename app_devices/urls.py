from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from app_devices.views import ImportReceiptData

app_name = 'devices'

urlpatterns = [
    path('import_receipt/', ImportReceiptData.as_view(), name='import_receipt'),
]
