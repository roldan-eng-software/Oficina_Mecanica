"""
Configuração do admin para os modelos de estoque.
"""
from django.contrib import admin
from .models import Fornecedor, Peca, MovimentacaoPeca


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    """Admin customizado para Fornecedor."""
    list_display = ['nome', 'contato', 'telefone', 'email', 'ativo', 'created_at']
    list_filter = ['ativo', 'created_at']
    search_fields = ['nome', 'contato', 'email', 'telefone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações do Fornecedor', {
            'fields': ('nome', 'contato', 'telefone', 'email')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    """Admin customizado para Peca."""
    list_display = ['codigo', 'descricao', 'categoria', 'quantidade_atual', 'quantidade_minima', 
                   'preco_venda', 'estoque_baixo', 'ativo', 'created_at']
    list_filter = ['categoria', 'ativo', 'fornecedor', 'created_at']
    search_fields = ['codigo', 'descricao', 'fabricante']
    readonly_fields = ['estoque_baixo', 'created_at', 'updated_at']
    fieldsets = (
        ('Informações da Peça', {
            'fields': ('codigo', 'descricao', 'fabricante', 'categoria', 'fornecedor')
        }),
        ('Preços', {
            'fields': ('preco_compra', 'preco_venda')
        }),
        ('Estoque', {
            'fields': ('quantidade_minima', 'quantidade_atual', 'estoque_baixo')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MovimentacaoPeca)
class MovimentacaoPecaAdmin(admin.ModelAdmin):
    """Admin customizado para MovimentacaoPeca."""
    list_display = ['peca', 'tipo', 'quantidade', 'data_movimentacao', 'usuario_responsavel', 'ativo', 'created_at']
    list_filter = ['tipo', 'ativo', 'data_movimentacao', 'created_at']
    search_fields = ['peca__codigo', 'peca__descricao', 'motivo']
    readonly_fields = ['data_movimentacao', 'created_at', 'updated_at']
    date_hierarchy = 'data_movimentacao'
    fieldsets = (
        ('Informações da Movimentação', {
            'fields': ('peca', 'tipo', 'quantidade', 'data_movimentacao', 'usuario_responsavel')
        }),
        ('Detalhes', {
            'fields': ('motivo',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

