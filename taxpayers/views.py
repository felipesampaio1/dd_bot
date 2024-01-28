from django.shortcuts import render
from django.views.generic import ListView
from .models import Payers


# Create your views here.


class AllTaxpayers(ListView):
    model: Payers
    template_name = "payers/index.html"
    queryset = Payers.objects.all()
