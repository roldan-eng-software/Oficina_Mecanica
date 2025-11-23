"""
Modelos base e principais do sistema de gestão de oficina mecânica.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from PIL import Image
import os


class BaseModel(models.Model):
    """
    Modelo abstrato base com campos comuns a todos os modelos.
    
    Campos:
        created_at: Data e hora de criação do registro
        updated_at: Data e hora da última atualização
        ativo: Indica se o registro está ativo no sistema
    """
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Data de Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Empresa(BaseModel):
    """
    Modelo para representar a empresa/oficina.
    
    Campos:
        nome: Nome da empresa
        cnpj: CNPJ único da empresa
        telefone: Telefone de contato
        email: Email de contato
        endereco: Endereço completo
        cidade: Cidade
        estado: Estado (UF)
        cep: CEP
        logo: Logo da empresa
    """
    cnpj_validator = RegexValidator(
        regex=r'^\d{14}$',
        message='CNPJ deve conter 14 dígitos numéricos'
    )

    nome = models.CharField('Nome', max_length=200)
    cnpj = models.CharField('CNPJ', max_length=14, unique=True, validators=[cnpj_validator])
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('Email')
    endereco = models.CharField('Endereço', max_length=300)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2)
    cep = models.CharField('CEP', max_length=10)
    logo = models.ImageField('Logo', upload_to='empresa/logos/', null=True, blank=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        """Redimensiona a logo se fornecida."""
        super().save(*args, **kwargs)
        if self.logo:
            img = Image.open(self.logo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.logo.path)


class Usuario(BaseModel):
    """
    Modelo para estender o usuário do Django com informações da oficina.
    
    Campos:
        user: Relacionamento OneToOne com User do Django
        empresa: Empresa à qual o usuário pertence
        role: Função do usuário no sistema
    """
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('gerente', 'Gerente'),
        ('mecanico', 'Mecânico'),
        ('atendente', 'Atendente'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_oficina')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuarios')
    role = models.CharField('Função', max_length=20, choices=ROLE_CHOICES, default='atendente')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"

