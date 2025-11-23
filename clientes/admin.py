"""
Configuração do admin para os modelos de clientes.
"""
from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin customizado para Cliente."""
    list_display = ['nome', 'cpf_cnpj', 'telefone', 'email', 'cidade', 'ativo', 'created_at']
    list_filter = ['ativo', 'estado', 'cidade', 'created_at']
    search_fields = ['nome', 'cpf_cnpj', 'email', 'telefone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cpf_cnpj', 'telefone', 'email')
        }),
        ('Endereço', {
            'fields': ('endereco', 'cidade', 'estado', 'cep')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

