from django.http import JsonResponse, HttpResponseRedirect
from django.template.defaultfilters import truncatechars_html
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView, TemplateView
from elq.mixin import BaseClassContextMixin


class IndexPageView(BaseClassContextMixin, TemplateView):
    title = 'Электронная очередь'
    template_name = 'app_main/index.html'

    def __init__(self, **kwargs):
        super(IndexPageView, self).__init__(**kwargs)
        self.object = None
        self.is_ajax = False

    def post(self, request, *args, **kwargs):
        self.is_ajax = True if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else False
        if self.is_ajax:
            return JsonResponse(
                {'result': 1, 'object': 'elq', 'data': render_to_string('app_main/inc/content.html')}
            )
