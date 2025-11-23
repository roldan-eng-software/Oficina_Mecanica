"""
Formulários do app veiculos.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Veiculo
from clientes.models import Cliente


class VeiculoForm(forms.ModelForm):
    """Formulário para Veiculo."""
    
    class Meta:
        model = Veiculo
        fields = ['cliente', 'placa', 'marca', 'modelo', 'ano', 'cor', 'chassis', 'status', 'ativo']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2100'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
            'chassis': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(ativo=True).order_by('nome')
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='form-group col-md-6'),
                Column('placa', css_class='form-group col-md-3'),
                Column('status', css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            Row(
                Column('marca', css_class='form-group col-md-4'),
                Column('modelo', css_class='form-group col-md-4'),
                Column('ano', css_class='form-group col-md-2'),
                Column('cor', css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            'chassis',
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )

    def clean_placa(self):
        """Validação e normalização da placa."""
        placa = self.cleaned_data.get('placa', '').upper().replace('-', '').replace(' ', '')
        return placa

