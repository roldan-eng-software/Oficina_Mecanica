"""
URLs do app estoque.
"""
from django.urls import path
from .views import (
    PecaListView, PecaDetailView, PecaCreateView, PecaUpdateView,
    MovimentacaoPecaListView, MovimentacaoPecaCreateView
)

app_name = 'estoque'

urlpatterns = [
    path('', PecaListView.as_view(), name='peca_list'),
    path('<int:pk>/', PecaDetailView.as_view(), name='peca_detail'),
    path('novo/', PecaCreateView.as_view(), name='peca_create'),
    path('<int:pk>/editar/', PecaUpdateView.as_view(), name='peca_update'),
    path('movimentacoes/', MovimentacaoPecaListView.as_view(), name='movimentacao_list'),
    path('movimentacoes/nova/', MovimentacaoPecaCreateView.as_view(), name='movimentacao_create'),
]

