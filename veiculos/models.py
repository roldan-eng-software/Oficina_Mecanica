"""
Modelos do app veiculos.
"""
from django.db import models
from django.core.validators import RegexValidator
from core.models import BaseModel
from clientes.models import Cliente


class Veiculo(BaseModel):
    """
    Modelo para representar um veículo.
    
    Campos:
        cliente: Cliente proprietário do veículo
        placa: Placa do veículo (única)
        marca: Marca do veículo
        modelo: Modelo do veículo
        ano: Ano de fabricação
        cor: Cor do veículo
        chassis: Número do chassi
        status: Status atual do veículo
    """
    STATUS_CHOICES = [
        ('em_uso', 'Em Uso'),
        ('em_manutencao', 'Em Manutenção'),
        ('descartado', 'Descartado'),
    ]

    placa_validator = RegexValidator(
        regex=r'^[A-Z]{3}\d{4}$|^[A-Z]{3}\d[A-Z]\d{2}$',
        message='Placa deve estar no formato ABC1234 ou ABC1D23 (Mercosul)'
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='veiculos')
    placa = models.CharField('Placa', max_length=8, unique=True, db_index=True, validators=[placa_validator])
    marca = models.CharField('Marca', max_length=50)
    modelo = models.CharField('Modelo', max_length=100)
    ano = models.PositiveIntegerField('Ano')
    cor = models.CharField('Cor', max_length=30, blank=True)
    chassis = models.CharField('Chassi', max_length=17, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='em_uso')

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['placa']

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

    @property
    def agendamentos_ativos(self):
        """Retorna os agendamentos ativos do veículo."""
        return self.agendamentos.filter(
            ativo=True,
            status__in=['agendado', 'em_progresso']
        )

