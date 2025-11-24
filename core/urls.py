"""
URLs do app core.
"""
from django.urls import path
from .views import DashboardView, create_superuser_view, reset_superuser_view

app_name = 'core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    # Views temporárias para gerenciar superusuário - REMOVER APÓS USO
    path('create-superuser/', create_superuser_view, name='create_superuser'),
    path('reset-superuser/', reset_superuser_view, name='reset_superuser'),
]

