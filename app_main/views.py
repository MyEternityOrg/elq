import datetime

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, TemplateView

from app_main.models import Document, Status
from elq.mixin import BaseClassContextMixin, UserLoginCheckMixin


class IndexPageView(BaseClassContextMixin, TemplateView):
    title = 'Управление электронной очередью'
    template_name = 'app_main/index.html'


class PanelPageView(BaseClassContextMixin, ListView):
    title = 'Электронная очередь'
    template_name = 'app_main/dashboard.html'
    model = Document

    def __init__(self, **kwargs):
        super(PanelPageView, self).__init__(**kwargs)
        self.object = None
        self.is_ajax = False

    def post(self, request, *args, **kwargs):
        self.is_ajax = True if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else False
        if self.is_ajax:
            return JsonResponse(
                {'result': 1, 'object': 'elq',
                 'data': render_to_string('app_main/inc/dashboard_content.html', {'object_list': self.get_queryset()})}
            )

    def get_queryset(self):
        return Document.objects.filter(status_id__in=Status.get_dashboard_statuses(),
                                       create_date=datetime.date.today()).order_by('create_time')

    def get_context_data(self, **kwargs):
        context = super(PanelPageView, self).get_context_data(**kwargs)
        return context


class DocumentListView(BaseClassContextMixin, UserLoginCheckMixin, ListView):
    template_name = 'app_main/documents.html'
    model = Document
    title = 'Список заказов'

    def __init__(self, **kwargs):
        super(DocumentListView, self).__init__(**kwargs)
        self.object = None
        self.is_ajax = False

    def get_queryset(self):
        return Document.objects.filter(status_id__in=Status.get_dashboard_statuses(),
                                       create_date=datetime.date.today()).order_by('create_time')

    def post(self, request, *args, **kwargs):
        self.is_ajax = True if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else False
        if self.is_ajax:
            full_update = True if request.POST.get('full_update', 0) == '1' else False
            if not full_update:
                self.object = Document.objects.filter(guid=request.POST.get('object', None)).first()
                status = Status.objects.filter(id=request.POST.get('next_status', -1)).first()
                self.object.status_id = status
                self.object.save()
                if status.finished == 1:
                    return JsonResponse({'result': 2, 'object': self.object.guid, 'data': ''})
                else:
                    return JsonResponse(
                        {'result': 1, 'object': self.object.guid,
                         "background_color": self.object.status_id.color,
                         'data': render_to_string('app_main/inc/document_row.html', {'object': self.object})}
                    )
            else:
                return JsonResponse(
                    {'result': 1, 'object': 'eld', 'data': render_to_string('app_main/inc/document_list.html', {
                        'object_list': self.get_queryset()})})
