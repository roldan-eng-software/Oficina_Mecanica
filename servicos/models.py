"""
Modelos do app servicos.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import BaseModel
from agendamentos.models import Agendamento


class Servico(BaseModel):
    """
    Modelo para representar um serviço realizado.
    
    Campos:
        agendamento: Agendamento relacionado (OneToOne)
        data_inicio: Data e hora de início do serviço
        data_fim: Data e hora de conclusão do serviço
        descricao_trabalho: Descrição detalhada do trabalho realizado
        preco_mao_obra: Preço da mão de obra
        desconto: Valor do desconto aplicado
        valor_total: Valor total do serviço
        status: Status atual do serviço
    """
    STATUS_CHOICES = [
        ('orcamento', 'Orçamento'),
        ('em_execucao', 'Em Execução'),
        ('concluido', 'Concluído'),
        ('faturado', 'Faturado'),
    ]

    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, related_name='servico')
    data_inicio = models.DateTimeField('Data de Início', null=True, blank=True)
    data_fim = models.DateTimeField('Data de Conclusão', null=True, blank=True)
    descricao_trabalho = models.TextField('Descrição do Trabalho', blank=True)
    preco_mao_obra = models.DecimalField('Preço Mão de Obra', max_digits=10, decimal_places=2, 
                                         default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    desconto = models.DecimalField('Desconto', max_digits=10, decimal_places=2, 
                                   default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2, 
                                     default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='orcamento')

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['-created_at']

    def __str__(self):
        return f"Serviço #{self.pk} - {self.agendamento.veiculo.placa}"

    def calcular_valor_total(self):
        """Calcula o valor total do serviço incluindo peças e mão de obra."""
        total_pecas = sum(item.subtotal for item in self.orcamentos.all())
        total = total_pecas + self.preco_mao_obra - self.desconto
        self.valor_total = max(total, Decimal('0.00'))
        return self.valor_total

    def save(self, *args, **kwargs):
        """Atualiza o valor total antes de salvar."""
        if not self.pk or 'preco_mao_obra' in kwargs.get('update_fields', []) or 'desconto' in kwargs.get('update_fields', []):
            self.calcular_valor_total()
        super().save(*args, **kwargs)

    def gerar_orcamento_pdf(self):
        """Gera um PDF do orçamento (implementação futura)."""
        # TODO: Implementar geração de PDF
        pass


class Orcamento(BaseModel):
    """
    Modelo para representar itens de orçamento de um serviço.
    
    Campos:
        servico: Serviço relacionado
        item: Descrição do item
        quantidade: Quantidade do item
        valor_unitario: Valor unitário do item
        subtotal: Subtotal do item (calculado)
    """
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='orcamentos')
    item = models.CharField('Item', max_length=200)
    quantidade = models.PositiveIntegerField('Quantidade', default=1, validators=[MinValueValidator(1)])
    valor_unitario = models.DecimalField('Valor Unitário', max_digits=10, decimal_places=2, 
                                        validators=[MinValueValidator(Decimal('0.00'))])
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, 
                                  default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['item']

    def __str__(self):
        return f"{self.item} - {self.quantidade}x"

    def calcular_subtotal(self):
        """Calcula o subtotal do item."""
        self.subtotal = self.quantidade * self.valor_unitario
        return self.subtotal

    def save(self, *args, **kwargs):
        """Atualiza o subtotal antes de salvar."""
        self.calcular_subtotal()
        super().save(*args, **kwargs)
        # Atualiza o valor total do serviço
        if self.servico:
            self.servico.calcular_valor_total()
            self.servico.save(update_fields=['valor_total'])

