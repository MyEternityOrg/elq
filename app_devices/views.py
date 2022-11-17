import json
from django.http import JsonResponse, HttpResponseRedirect
from django.template.defaultfilters import truncatechars_html
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView, TemplateView
from elq.mixin import BaseClassContextMixin
from app_devices.models import ImportedChecks
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from elq.settings import API_KEY


@method_decorator(csrf_exempt, name='dispatch')
class ImportReceiptData(BaseClassContextMixin, CreateView):
    title = 'Импорт данных кассовых чеков'
    template_name = 'app_devices/import_receipt_data.html'
    model = ImportedChecks
    fields = ['cash_id']

    def post(self, request, *args, **kwargs):
        json_reply_error = ""
        if self.request.headers.get('key', None) == API_KEY:
            try:
                json_input = json.loads(self.request.body)
                if type(json_input) is dict:
                    result, msg, cash_guid = ImportedChecks.register_cash_check(json_input.get('cash_id', 0),
                                                                     json_input.get('check_id', 0),
                                                                     json_input.get('check_date', now))
                    if result:
                        print(json_input)
                    else:
                        print(msg)
            except Exception as E:
                json_reply_error = f'{E}'
        else:
            json_reply_error = 'Invalid api key.'
        return JsonResponse({"error": json_reply_error})

    def get_context_data(self, **kwargs):
        context = super(ImportReceiptData, self).get_context_data(**kwargs)
        return context
