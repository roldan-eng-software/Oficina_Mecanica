"""
URLs do app servicos.
"""
from django.urls import path
from .views import (
    ServicoListView, ServicoDetailView, ServicoCreateView,
    ServicoUpdateView, OrcamentoListView, OrcamentoDetailView
)

app_name = 'servicos'

urlpatterns = [
    path('', ServicoListView.as_view(), name='servico_list'),
    path('<int:pk>/', ServicoDetailView.as_view(), name='servico_detail'),
    path('novo/', ServicoCreateView.as_view(), name='servico_create'),
    path('<int:pk>/editar/', ServicoUpdateView.as_view(), name='servico_update'),
    path('orcamentos/', OrcamentoListView.as_view(), name='orcamento_list'),
    path('orcamentos/<int:pk>/', OrcamentoDetailView.as_view(), name='orcamento_detail'),
]

