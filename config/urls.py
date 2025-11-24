"""
URL configuration for Oficina Mecanica project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('clientes/', include('clientes.urls')),
    path('veiculos/', include('veiculos.urls')),
    path('agendamentos/', include('agendamentos.urls')),
    path('servicos/', include('servicos.urls')),
    path('estoque/', include('estoque.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('relatorios/', include('relatorios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

