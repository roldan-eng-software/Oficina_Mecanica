"""
Modelos do app agendamentos.
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta
from core.models import BaseModel
from clientes.models import Cliente
from veiculos.models import Veiculo
from core.models import Usuario


class Agendamento(BaseModel):
    """
    Modelo para representar um agendamento de serviço.
    
    Campos:
        veiculo: Veículo a ser atendido
        cliente: Cliente proprietário
        data_hora: Data e hora do agendamento
        mecanico: Mecânico responsável
        descricao_problema: Descrição do problema relatado
        status: Status atual do agendamento
    """
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('em_progresso', 'Em Progresso'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='agendamentos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    data_hora = models.DateTimeField('Data e Hora')
    mecanico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='agendamentos', limit_choices_to={'role__in': ['mecanico', 'gerente', 'admin']})
    descricao_problema = models.TextField('Descrição do Problema', blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='agendado')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.veiculo.placa} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def marcar_como_concluido(self):
        """Marca o agendamento como concluído."""
        self.status = 'concluido'
        self.save()

    def calcular_duracao(self):
        """Calcula a duração do serviço se houver serviço associado."""
        if hasattr(self, 'servico') and self.servico.data_inicio and self.servico.data_fim:
            return self.servico.data_fim - self.servico.data_inicio
        return None

    def get_tempo_restante(self):
        """Retorna o tempo restante até o agendamento."""
        if self.status == 'agendado' and self.data_hora > timezone.now():
            return self.data_hora - timezone.now()
        return None

    @property
    def esta_proximo(self):
        """Verifica se o agendamento está próximo (menos de 24 horas)."""
        if self.status == 'agendado':
            tempo_restante = self.get_tempo_restante()
            if tempo_restante and tempo_restante <= timedelta(hours=24):
                return True
        return False

