"""
Formulários do app agendamentos.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Agendamento
from clientes.models import Cliente
from veiculos.models import Veiculo
from core.models import Usuario


class AgendamentoForm(forms.ModelForm):
    """Formulário para Agendamento."""
    
    class Meta:
        model = Agendamento
        fields = ['veiculo', 'cliente', 'data_hora', 'mecanico', 'descricao_problema', 'status', 'ativo']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'data_hora': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'mecanico': forms.Select(attrs={'class': 'form-select'}),
            'descricao_problema': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veiculo'].queryset = Veiculo.objects.filter(ativo=True).order_by('placa')
        self.fields['cliente'].queryset = Cliente.objects.filter(ativo=True).order_by('nome')
        self.fields['mecanico'].queryset = Usuario.objects.filter(
            ativo=True,
            role__in=['mecanico', 'gerente', 'admin']
        ).select_related('user').order_by('user__first_name', 'user__last_name')
        
        # Formatar o campo de data_hora para datetime-local
        if self.instance and self.instance.pk and self.instance.data_hora:
            self.initial['data_hora'] = self.instance.data_hora.strftime('%Y-%m-%dT%H:%M')
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('veiculo', css_class='form-group col-md-6'),
                Column('cliente', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('data_hora', css_class='form-group col-md-6'),
                Column('mecanico', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'descricao_problema',
            Row(
                Column('status', css_class='form-group col-md-6'),
                Column('ativo', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )

