"""
URLs do app agendamentos.
"""
from django.urls import path
from .views import (
    AgendamentoListView, AgendamentoDetailView, AgendamentoCreateView,
    AgendamentoUpdateView, AgendamentoDeleteView, CalendarioView
)

app_name = 'agendamentos'

urlpatterns = [
    path('', AgendamentoListView.as_view(), name='agendamento_list'),
    path('calendario/', CalendarioView.as_view(), name='calendario'),
    path('<int:pk>/', AgendamentoDetailView.as_view(), name='agendamento_detail'),
    path('novo/', AgendamentoCreateView.as_view(), name='agendamento_create'),
    path('<int:pk>/editar/', AgendamentoUpdateView.as_view(), name='agendamento_update'),
    path('<int:pk>/excluir/', AgendamentoDeleteView.as_view(), name='agendamento_delete'),
]

