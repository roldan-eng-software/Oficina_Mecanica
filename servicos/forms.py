"""
Formulários do app servicos.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Fieldset
from .models import Servico, Orcamento
from agendamentos.models import Agendamento


class OrcamentoForm(forms.ModelForm):
    """Formulário inline para Orcamento."""
    
    class Meta:
        model = Orcamento
        fields = ['item', 'quantidade', 'valor_unitario']
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
        }


class ServicoForm(forms.ModelForm):
    """Formulário para Servico."""
    
    class Meta:
        model = Servico
        fields = ['agendamento', 'data_inicio', 'data_fim', 'descricao_trabalho', 
                  'preco_mao_obra', 'desconto', 'status', 'ativo']
        widgets = {
            'agendamento': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'data_fim': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'descricao_trabalho': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'preco_mao_obra': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'desconto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agendamento'].queryset = Agendamento.objects.filter(
            ativo=True
        ).select_related('veiculo', 'cliente').order_by('-data_hora')
        
        # Formatar campos de data
        if self.instance and self.instance.pk:
            if self.instance.data_inicio:
                self.initial['data_inicio'] = self.instance.data_inicio.strftime('%Y-%m-%dT%H:%M')
            if self.instance.data_fim:
                self.initial['data_fim'] = self.instance.data_fim.strftime('%Y-%m-%dT%H:%M')
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Informações do Serviço',
                Row(
                    Column('agendamento', css_class='form-group col-md-6'),
                    Column('status', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
                Row(
                    Column('data_inicio', css_class='form-group col-md-6'),
                    Column('data_fim', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'Descrição e Valores',
                'descricao_trabalho',
                Row(
                    Column('preco_mao_obra', css_class='form-group col-md-6'),
                    Column('desconto', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
            ),
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )

