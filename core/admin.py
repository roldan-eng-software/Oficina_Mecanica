"""
Configuração do admin para os modelos do core.
"""
from django.contrib import admin
from .models import Empresa, Usuario


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    """Admin customizado para Empresa."""
    list_display = ['nome', 'cnpj', 'cidade', 'estado', 'telefone', 'ativo', 'created_at']
    list_filter = ['ativo', 'estado', 'created_at']
    search_fields = ['nome', 'cnpj', 'email', 'cidade']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cnpj', 'logo')
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
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


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """Admin customizado para Usuario."""
    list_display = ['user', 'empresa', 'role', 'ativo', 'created_at']
    list_filter = ['role', 'ativo', 'empresa', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Usuário', {
            'fields': ('user', 'empresa', 'role')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

