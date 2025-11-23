"""
URLs do app veiculos.
"""
from django.urls import path
from .views import (
    VeiculoListView, VeiculoDetailView, VeiculoCreateView,
    VeiculoUpdateView, VeiculoDeleteView
)

app_name = 'veiculos'

urlpatterns = [
    path('', VeiculoListView.as_view(), name='veiculo_list'),
    path('<int:pk>/', VeiculoDetailView.as_view(), name='veiculo_detail'),
    path('novo/', VeiculoCreateView.as_view(), name='veiculo_create'),
    path('<int:pk>/editar/', VeiculoUpdateView.as_view(), name='veiculo_update'),
    path('<int:pk>/excluir/', VeiculoDeleteView.as_view(), name='veiculo_delete'),
]

