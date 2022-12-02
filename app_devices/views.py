import json
from django.http import JsonResponse, HttpResponseRedirect
from django.template.defaultfilters import truncatechars_html
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView, TemplateView
from elq.mixin import BaseClassContextMixin
from app_devices.models import ImportedChecks, Printer
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from elq.settings import API_KEY


@method_decorator(csrf_exempt, name='dispatch')
class ImportReceiptData(BaseClassContextMixin, TemplateView):
    title = 'Импорт данных кассовых чеков'
    template_name = 'app_devices/import_receipt_data.html'
    model = ImportedChecks

    def post(self, request, *args, **kwargs):
        json_reply_error = ""
        json_reply_number = -1
        doc_count = 0
        if self.request.headers.get('key', None) == API_KEY:
            try:
                json_input = json.loads(self.request.body)
                print(f'Receive data : {json_input}')
                if type(json_input) is dict:
                    result, msg, json_reply_number, printer, doc_count = ImportedChecks.register_cash_check(
                        json_input.get('cash_id', 0),
                        json_input.get('shift_id', 1),
                        json_input.get('check_id', 0),
                        json_input.get('check_date',
                                       now),
                        json_input.get('wares', []))
                    if result:
                        Printer.print_document(printer, json_reply_number, json_input.get('check_date', now), doc_count)
                    else:
                        json_reply_error = msg
            except Exception as E:
                print(E)
                json_reply_error = f'{E}'
        else:
            json_reply_error = 'Invalid api key.'
        print(f'Send reply: "doc_number": {json_reply_number}, "count": {doc_count}, "error": {json_reply_error}')
        return JsonResponse({"doc_number": json_reply_number, "count": doc_count, "error": json_reply_error})

    def get_context_data(self, **kwargs):
        context = super(ImportReceiptData, self).get_context_data(**kwargs)
        return context
