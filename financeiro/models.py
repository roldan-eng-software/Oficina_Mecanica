"""
Modelos do app financeiro.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from core.models import BaseModel
from servicos.models import Servico
from clientes.models import Cliente
from estoque.models import Fornecedor


class ContaReceber(BaseModel):
    """
    Modelo para representar contas a receber.
    
    Campos:
        servico: Serviço relacionado
        cliente: Cliente devedor
        valor: Valor da conta
        data_vencimento: Data de vencimento
        data_pagamento: Data de pagamento (nullable)
        status: Status da conta
    """
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('paga', 'Paga'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='contas_receber', null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contas_receber')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2, 
                               validators=[MinValueValidator(Decimal('0.01'))])
    data_vencimento = models.DateField('Data de Vencimento')
    data_pagamento = models.DateField('Data de Pagamento', null=True, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='aberta')

    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['-data_vencimento']

    def __str__(self):
        return f"Conta #{self.pk} - {self.cliente.nome} - R$ {self.valor}"

    @property
    def dias_em_atraso(self):
        """Calcula quantos dias a conta está em atraso."""
        if self.status == 'aberta' and self.data_vencimento < timezone.now().date():
            return (timezone.now().date() - self.data_vencimento).days
        return 0

    def marcar_como_paga(self, data_pagamento=None):
        """Marca a conta como paga."""
        self.status = 'paga'
        self.data_pagamento = data_pagamento or timezone.now().date()
        self.save()

    def gerar_aviso_vencimento(self):
        """Gera aviso de vencimento (implementação futura)."""
        # TODO: Implementar envio de email/SMS
        pass


class ContaPagar(BaseModel):
    """
    Modelo para representar contas a pagar.
    
    Campos:
        fornecedor: Fornecedor credor
        descricao: Descrição da conta
        valor: Valor da conta
        data_vencimento: Data de vencimento
        data_pagamento: Data de pagamento (nullable)
        status: Status da conta
        categoria: Categoria da despesa
    """
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('paga', 'Paga'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]

    CATEGORIA_CHOICES = [
        ('pecas', 'Peças'),
        ('servicos', 'Serviços'),
        ('salarios', 'Salários'),
        ('aluguel', 'Aluguel'),
        ('utilitarios', 'Utilidades'),
        ('outros', 'Outros'),
    ]

    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='contas_pagar')
    descricao = models.CharField('Descrição', max_length=200)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2, 
                               validators=[MinValueValidator(Decimal('0.01'))])
    data_vencimento = models.DateField('Data de Vencimento')
    data_pagamento = models.DateField('Data de Pagamento', null=True, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='aberta')
    categoria = models.CharField('Categoria', max_length=20, choices=CATEGORIA_CHOICES, default='outros')

    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['-data_vencimento']

    def __str__(self):
        return f"Conta #{self.pk} - {self.descricao} - R$ {self.valor}"

    @property
    def dias_em_atraso(self):
        """Calcula quantos dias a conta está em atraso."""
        if self.status == 'aberta' and self.data_vencimento < timezone.now().date():
            return (timezone.now().date() - self.data_vencimento).days
        return 0

    def marcar_como_paga(self, data_pagamento=None):
        """Marca a conta como paga."""
        self.status = 'paga'
        self.data_pagamento = data_pagamento or timezone.now().date()
        self.save()


class PagamentoServico(BaseModel):
    """
    Modelo para representar pagamentos de serviços.
    
    Campos:
        servico: Serviço relacionado
        forma_pagamento: Forma de pagamento utilizada
        valor: Valor pago
        data: Data do pagamento
    """
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('cheque', 'Cheque'),
        ('transferencia', 'Transferência'),
    ]

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='pagamentos')
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2, 
                               validators=[MinValueValidator(Decimal('0.01'))])
    data = models.DateField('Data do Pagamento', default=timezone.now)

    class Meta:
        verbose_name = 'Pagamento de Serviço'
        verbose_name_plural = 'Pagamentos de Serviços'
        ordering = ['-data']

    def __str__(self):
        return f"Pagamento #{self.pk} - {self.servico} - R$ {self.valor}"

    @property
    def valor_total_pago(self):
        """Retorna o valor total pago do serviço."""
        from django.db.models import Sum
        return self.servico.pagamentos.aggregate(
            total=Sum('valor')
        )['total'] or Decimal('0.00')

