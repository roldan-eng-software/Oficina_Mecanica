from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('clientes/', views.clientes_print, name='clientes_print'),
    path('clientes/pdf/', views.clientes_pdf, name='clientes_pdf'),
    path('veiculos/', views.veiculos_print, name='veiculos_print'),
    path('veiculos/pdf/', views.veiculos_pdf, name='veiculos_pdf'),
    path('agendamentos/', views.agendamentos_print, name='agendamentos_print'),
    path('agendamentos/pdf/', views.agendamentos_pdf, name='agendamentos_pdf'),
    path('servicos/', views.servicos_print, name='servicos_print'),
    path('servicos/pdf/', views.servicos_pdf, name='servicos_pdf'),
    path('estoque/', views.estoque_print, name='estoque_print'),
    path('estoque/pdf/', views.estoque_pdf, name='estoque_pdf'),
    path('financeiro/', views.financeiro_print, name='financeiro_print'),
    path('financeiro/pdf/', views.financeiro_pdf, name='financeiro_pdf'),
]
