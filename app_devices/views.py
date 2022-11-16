from django.http import JsonResponse, HttpResponseRedirect
from django.template.defaultfilters import truncatechars_html
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView, TemplateView
from elq.mixin import BaseClassContextMixin
from app_devices.models import ImportedChecks
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ImportReceiptData(BaseClassContextMixin, CreateView):
    title = 'Импорт данных кассовых чеков'
    template_name = 'app_devices/import_receipt_data.html'
    model = ImportedChecks
    fields = ['cash_id', 'check_id']

    def post(self, request, *args, **kwargs):
        print(request)
        print(*args)
        return JsonResponse({"error": "none"})

    def get_context_data(self, **kwargs):
        context = super(ImportReceiptData, self).get_context_data(**kwargs)
        return context
