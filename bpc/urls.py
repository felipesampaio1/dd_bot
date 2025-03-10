from django.urls import path
from . import views

app_name = 'bpc'

urlpatterns = [
    path('consultar/<uuid:payer_id>/', views.consultar_bpc, name='consultar_bpc'),
]