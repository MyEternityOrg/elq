from django.http import JsonResponse, HttpResponseRedirect
from django.template.defaultfilters import truncatechars_html
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView, TemplateView
