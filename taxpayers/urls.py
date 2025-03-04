from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_payers, name='list_payers'),
    path('adicionar/', views.add_payer, name='add_payer'),
    path('editar/<uuid:id>/', views.edit_payer, name='edit_payer'),
    path('deletar/<uuid:id>/', views.delete_payer, name='delete_payer'),
]
