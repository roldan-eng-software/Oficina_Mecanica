"""
Modelos do app estoque.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import BaseModel
from core.models import Usuario


class Fornecedor(BaseModel):
    """
    Modelo para representar um fornecedor de peças.
    
    Campos:
        nome: Nome do fornecedor
        contato: Nome do contato
        email: Email de contato
        telefone: Telefone de contato
    """
    nome = models.CharField('Nome', max_length=200)
    contato = models.CharField('Contato', max_length=100, blank=True)
    email = models.EmailField('Email', blank=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Peca(BaseModel):
    """
    Modelo para representar uma peça no estoque.
    
    Campos:
        codigo: Código único da peça
        descricao: Descrição da peça
        fabricante: Fabricante da peça
        categoria: Categoria da peça
        preco_compra: Preço de compra
        preco_venda: Preço de venda
        quantidade_minima: Quantidade mínima em estoque
        quantidade_atual: Quantidade atual em estoque
        fornecedor: Fornecedor principal
    """
    CATEGORIA_CHOICES = [
        ('motor', 'Motor'),
        ('freios', 'Freios'),
        ('suspensao', 'Suspensão'),
        ('transmissao', 'Transmissão'),
        ('eletrica', 'Elétrica'),
        ('carroceria', 'Carroceria'),
        ('outro', 'Outro'),
    ]

    codigo = models.CharField('Código', max_length=50, unique=True, db_index=True)
    descricao = models.CharField('Descrição', max_length=200)
    fabricante = models.CharField('Fabricante', max_length=100, blank=True)
    categoria = models.CharField('Categoria', max_length=20, choices=CATEGORIA_CHOICES, default='outro')
    preco_compra = models.DecimalField('Preço de Compra', max_digits=10, decimal_places=2, 
                                       default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    preco_venda = models.DecimalField('Preço de Venda', max_digits=10, decimal_places=2, 
                                     default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    quantidade_minima = models.PositiveIntegerField('Quantidade Mínima', default=0)
    quantidade_atual = models.PositiveIntegerField('Quantidade Atual', default=0)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='pecas')

    class Meta:
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'
        ordering = ['descricao']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

    @property
    def estoque_baixo(self):
        """Verifica se o estoque está abaixo do mínimo."""
        return self.quantidade_atual <= self.quantidade_minima

    def atualizar_estoque(self, quantidade, tipo='entrada'):
        """
        Atualiza a quantidade em estoque.
        
        Args:
            quantidade: Quantidade a adicionar ou remover
            tipo: 'entrada' para adicionar, 'saida' para remover
        """
        if tipo == 'entrada':
            self.quantidade_atual += quantidade
        elif tipo == 'saida':
            if self.quantidade_atual >= quantidade:
                self.quantidade_atual -= quantidade
            else:
                raise ValueError('Quantidade insuficiente em estoque')
        self.save()


class MovimentacaoPeca(BaseModel):
    """
    Modelo para representar movimentações de peças no estoque.
    
    Campos:
        peca: Peça movimentada
        tipo: Tipo de movimentação (entrada/saida)
        quantidade: Quantidade movimentada
        data_movimentacao: Data da movimentação
        motivo: Motivo da movimentação
        usuario_responsavel: Usuário responsável pela movimentação
    """
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    peca = models.ForeignKey(Peca, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField('Tipo', max_length=10, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField('Quantidade', validators=[MinValueValidator(1)])
    data_movimentacao = models.DateTimeField('Data da Movimentação', auto_now_add=True)
    motivo = models.CharField('Motivo', max_length=200, blank=True)
    usuario_responsavel = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, 
                                           related_name='movimentacoes_estoque')

    class Meta:
        verbose_name = 'Movimentação de Peça'
        verbose_name_plural = 'Movimentações de Peças'
        ordering = ['-data_movimentacao']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.peca.codigo} - {self.quantidade}"

    def save(self, *args, **kwargs):
        """Atualiza o estoque ao salvar a movimentação."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Atualiza o estoque da peça
            self.peca.atualizar_estoque(self.quantidade, self.tipo)

