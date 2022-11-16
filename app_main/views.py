import datetime

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView

from app_main.models import Document, Status
from elq.mixin import BaseClassContextMixin


class IndexPageView(BaseClassContextMixin, ListView):
    title = 'Электронная очередь'
    template_name = 'app_main/index.html'
    model = Document

    def __init__(self, **kwargs):
        super(IndexPageView, self).__init__(**kwargs)
        self.object = None
        self.is_ajax = False

    def post(self, request, *args, **kwargs):
        self.is_ajax = True if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else False
        if self.is_ajax:
            return JsonResponse(
                {'result': 1, 'object': 'elq',
                 'data': render_to_string('app_main/inc/content.html', {'object_list': self.get_queryset()})}
            )

    def get_queryset(self):
        return Document.objects.filter(status_id__in=Status.get_dashboard_statuses(),
                                       create_date=datetime.date.today()).order_by('create_time')

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        return context
