"""
Configuração do admin para os modelos de agendamentos.
"""
from django.contrib import admin
from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    """Admin customizado para Agendamento."""
    list_display = ['veiculo', 'cliente', 'data_hora', 'mecanico', 'status', 'ativo', 'created_at']
    list_filter = ['status', 'ativo', 'data_hora', 'created_at']
    search_fields = ['veiculo__placa', 'cliente__nome', 'descricao_problema']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'data_hora'
    fieldsets = (
        ('Informações do Agendamento', {
            'fields': ('veiculo', 'cliente', 'data_hora', 'mecanico', 'status')
        }),
        ('Descrição', {
            'fields': ('descricao_problema',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

