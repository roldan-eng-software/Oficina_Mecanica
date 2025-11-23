"""
Formulários do app estoque.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Peca, MovimentacaoPeca, Fornecedor
from core.models import Usuario


class FornecedorForm(forms.ModelForm):
    """Formulário para Fornecedor."""
    
    class Meta:
        model = Fornecedor
        fields = ['nome', 'contato', 'email', 'telefone', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'data-mask': 'phone'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-8'),
                Column('contato', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('telefone', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )


class PecaForm(forms.ModelForm):
    """Formulário para Peca."""
    
    class Meta:
        model = Peca
        fields = ['codigo', 'descricao', 'fabricante', 'categoria', 'preco_compra', 
                 'preco_venda', 'quantidade_minima', 'quantidade_atual', 'fornecedor', 'ativo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'quantidade_minima': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'quantidade_atual': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True).order_by('nome')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='form-group col-md-4'),
                Column('categoria', css_class='form-group col-md-4'),
                Column('fornecedor', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('descricao', css_class='form-group col-md-8'),
                Column('fabricante', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('preco_compra', css_class='form-group col-md-4'),
                Column('preco_venda', css_class='form-group col-md-4'),
                Column('quantidade_minima', css_class='form-group col-md-2'),
                Column('quantidade_atual', css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )


class MovimentacaoPecaForm(forms.ModelForm):
    """Formulário para MovimentacaoPeca."""
    
    class Meta:
        model = MovimentacaoPeca
        fields = ['peca', 'tipo', 'quantidade', 'motivo', 'usuario_responsavel', 'ativo']
        widgets = {
            'peca': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_responsavel': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['peca'].queryset = Peca.objects.filter(ativo=True).order_by('descricao')
        self.fields['usuario_responsavel'].queryset = Usuario.objects.filter(ativo=True).select_related('user').order_by('user__first_name')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('peca', css_class='form-group col-md-6'),
                Column('tipo', css_class='form-group col-md-3'),
                Column('quantidade', css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            'motivo',
            'usuario_responsavel',
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )

