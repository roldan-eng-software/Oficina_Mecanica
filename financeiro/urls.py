"""
URLs do app financeiro.
"""
from django.urls import path
from .views import (
    ContaReceberListView, ContaPagarListView,
    ContaReceberCreateView, ContaPagarCreateView,
    DashboardFinanceiroView, RelatorioFinanceiroView
)

app_name = 'financeiro'

urlpatterns = [
    path('', DashboardFinanceiroView.as_view(), name='dashboard'),
    path('contas-receber/', ContaReceberListView.as_view(), name='conta_receber_list'),
    path('contas-pagar/', ContaPagarListView.as_view(), name='conta_pagar_list'),
    path('contas-receber/nova/', ContaReceberCreateView.as_view(), name='conta_receber_create'),
    path('contas-pagar/nova/', ContaPagarCreateView.as_view(), name='conta_pagar_create'),
    path('relatorio/', RelatorioFinanceiroView.as_view(), name='relatorio'),
]

