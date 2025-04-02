from django.urls import path
from .views import config_view

urlpatterns = [
    path('', config_view, name='config'),
]