"""
Configuração do admin para os modelos de veículos.
"""
from django.contrib import admin
from .models import Veiculo


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    """Admin customizado para Veiculo."""
    list_display = ['placa', 'marca', 'modelo', 'ano', 'cliente', 'status', 'ativo', 'created_at']
    list_filter = ['status', 'ativo', 'marca', 'ano', 'created_at']
    search_fields = ['placa', 'marca', 'modelo', 'chassis', 'cliente__nome']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('cliente', 'placa', 'marca', 'modelo', 'ano', 'cor', 'chassis')
        }),
        ('Status', {
            'fields': ('status', 'ativo')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

