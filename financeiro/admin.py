"""
Configuração do admin para os modelos financeiros.
"""
from django.contrib import admin
from .models import ContaReceber, ContaPagar, PagamentoServico


@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    """Admin customizado para ContaReceber."""
    list_display = ['id', 'cliente', 'valor', 'data_vencimento', 'data_pagamento', 'status', 'dias_em_atraso', 'ativo', 'created_at']
    list_filter = ['status', 'ativo', 'data_vencimento', 'created_at']
    search_fields = ['cliente__nome', 'servico__agendamento__veiculo__placa']
    readonly_fields = ['dias_em_atraso', 'created_at', 'updated_at']
    date_hierarchy = 'data_vencimento'
    fieldsets = (
        ('Informações da Conta', {
            'fields': ('servico', 'cliente', 'valor', 'data_vencimento', 'data_pagamento', 'status')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    """Admin customizado para ContaPagar."""
    list_display = ['id', 'descricao', 'fornecedor', 'valor', 'data_vencimento', 'data_pagamento', 'status', 'categoria', 'ativo', 'created_at']
    list_filter = ['status', 'categoria', 'ativo', 'data_vencimento', 'created_at']
    search_fields = ['descricao', 'fornecedor__nome']
    readonly_fields = ['dias_em_atraso', 'created_at', 'updated_at']
    date_hierarchy = 'data_vencimento'
    fieldsets = (
        ('Informações da Conta', {
            'fields': ('fornecedor', 'descricao', 'valor', 'categoria', 'data_vencimento', 'data_pagamento', 'status')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PagamentoServico)
class PagamentoServicoAdmin(admin.ModelAdmin):
    """Admin customizado para PagamentoServico."""
    list_display = ['id', 'servico', 'forma_pagamento', 'valor', 'data', 'ativo', 'created_at']
    list_filter = ['forma_pagamento', 'ativo', 'data', 'created_at']
    search_fields = ['servico__agendamento__veiculo__placa', 'servico__agendamento__cliente__nome']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações do Pagamento', {
            'fields': ('servico', 'forma_pagamento', 'valor', 'data')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

