from django.http import JsonResponse, HttpResponseRedirect
from django.template.defaultfilters import truncatechars_html
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView, TemplateView
from mixin import BaseClassContextMixin


class IndexPageView(BaseClassContextMixin, TemplateView):
    title = 'Электронная очередь'
    template_name = 'app_main/app_main_common.html'
