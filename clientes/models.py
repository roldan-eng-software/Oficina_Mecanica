"""
Modelos do app clientes.
"""
from django.db import models
from django.core.validators import RegexValidator
from core.models import BaseModel


class Cliente(BaseModel):
    """
    Modelo para representar um cliente da oficina.
    
    Campos:
        nome: Nome completo do cliente
        cpf_cnpj: CPF ou CNPJ único do cliente
        email: Email de contato
        telefone: Telefone de contato
        endereco: Endereço completo
        cidade: Cidade
        estado: Estado (UF)
        cep: CEP
    """
    cpf_cnpj_validator = RegexValidator(
        regex=r'^\d{11,14}$',
        message='CPF/CNPJ deve conter entre 11 e 14 dígitos numéricos'
    )

    nome = models.CharField('Nome', max_length=100, db_index=True)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=20, unique=True, validators=[cpf_cnpj_validator])
    email = models.EmailField('Email', blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=20)
    endereco = models.CharField('Endereço', max_length=300, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    estado = models.CharField('Estado', max_length=2, blank=True)
    cep = models.CharField('CEP', max_length=10, blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def veiculos_ativos(self):
        """Retorna os veículos ativos do cliente."""
        return self.veiculos.filter(ativo=True)

    @property
    def total_veiculos(self):
        """Retorna o total de veículos do cliente."""
        return self.veiculos.count()

