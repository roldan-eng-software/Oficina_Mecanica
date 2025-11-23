"""
URLs do app clientes.
"""
from django.urls import path
from .views import (
    ClienteListView, ClienteDetailView, ClienteCreateView,
    ClienteUpdateView, ClienteDeleteView
)

app_name = 'clientes'

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list'),
    path('<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),
    path('novo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('<int:pk>/excluir/', ClienteDeleteView.as_view(), name='cliente_delete'),
]

