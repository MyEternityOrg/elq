from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import *

app_name = 'main'

urlpatterns = [
    path('', DocumentListView.as_view(), name='index'),
    path('dashboard/', PanelPageView.as_view(), name='dashboard'),
    path('documents/', DocumentListView.as_view(), name='documents'),
]
