"""
Formulários do app financeiro.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import ContaReceber, ContaPagar, PagamentoServico
from servicos.models import Servico
from clientes.models import Cliente
from estoque.models import Fornecedor


class ContaReceberForm(forms.ModelForm):
    """Formulário para ContaReceber."""
    
    class Meta:
        model = ContaReceber
        fields = ['servico', 'cliente', 'valor', 'data_vencimento', 'data_pagamento', 'status', 'ativo']
        widgets = {
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0.01}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servico'].queryset = Servico.objects.filter(ativo=True).select_related('agendamento__veiculo', 'agendamento__cliente')
        self.fields['cliente'].queryset = Cliente.objects.filter(ativo=True).order_by('nome')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('servico', css_class='form-group col-md-6'),
                Column('cliente', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('valor', css_class='form-group col-md-4'),
                Column('data_vencimento', css_class='form-group col-md-4'),
                Column('status', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            'data_pagamento',
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )


class ContaPagarForm(forms.ModelForm):
    """Formulário para ContaPagar."""
    
    class Meta:
        model = ContaPagar
        fields = ['fornecedor', 'descricao', 'valor', 'data_vencimento', 'data_pagamento', 'status', 'categoria', 'ativo']
        widgets = {
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0.01}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True).order_by('nome')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('fornecedor', css_class='form-group col-md-6'),
                Column('categoria', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'descricao',
            Row(
                Column('valor', css_class='form-group col-md-4'),
                Column('data_vencimento', css_class='form-group col-md-4'),
                Column('status', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            'data_pagamento',
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )


class PagamentoServicoForm(forms.ModelForm):
    """Formulário para PagamentoServico."""
    
    class Meta:
        model = PagamentoServico
        fields = ['servico', 'forma_pagamento', 'valor', 'data', 'ativo']
        widgets = {
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0.01}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servico'].queryset = Servico.objects.filter(ativo=True).select_related('agendamento__veiculo', 'agendamento__cliente')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('servico', css_class='form-group col-md-6'),
                Column('forma_pagamento', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('valor', css_class='form-group col-md-6'),
                Column('data', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )

