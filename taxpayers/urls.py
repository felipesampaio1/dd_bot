from django.urls import path
from . import views


urlpatterns = [
    path("", views.AllTaxpayers.as_view(), name="index")
]
