"""
Configuração do admin para os modelos de serviços.
"""
from django.contrib import admin
from .models import Servico, Orcamento


class OrcamentoInline(admin.TabularInline):
    """Inline admin para Orcamento."""
    model = Orcamento
    extra = 1
    fields = ['item', 'quantidade', 'valor_unitario', 'subtotal']


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    """Admin customizado para Servico."""
    list_display = ['id', 'agendamento', 'status', 'valor_total', 'data_inicio', 'data_fim', 'ativo', 'created_at']
    list_filter = ['status', 'ativo', 'data_inicio', 'created_at']
    search_fields = ['agendamento__veiculo__placa', 'agendamento__cliente__nome', 'descricao_trabalho']
    readonly_fields = ['valor_total', 'created_at', 'updated_at']
    inlines = [OrcamentoInline]
    fieldsets = (
        ('Informações do Serviço', {
            'fields': ('agendamento', 'status', 'data_inicio', 'data_fim')
        }),
        ('Descrição', {
            'fields': ('descricao_trabalho',)
        }),
        ('Valores', {
            'fields': ('preco_mao_obra', 'desconto', 'valor_total')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    """Admin customizado para Orcamento."""
    list_display = ['item', 'servico', 'quantidade', 'valor_unitario', 'subtotal', 'ativo', 'created_at']
    list_filter = ['ativo', 'created_at']
    search_fields = ['item', 'servico__agendamento__veiculo__placa']
    readonly_fields = ['subtotal', 'created_at', 'updated_at']
    fieldsets = (
        ('Informações do Item', {
            'fields': ('servico', 'item', 'quantidade', 'valor_unitario', 'subtotal')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

