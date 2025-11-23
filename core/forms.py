"""
Formulários do app core.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Empresa, Usuario


class EmpresaForm(forms.ModelForm):
    """Formulário para Empresa."""
    
    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj', 'telefone', 'email', 'endereco', 
                  'cidade', 'estado', 'cep', 'logo', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000000000000'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-8'),
                Column('cnpj', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('telefone', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'endereco',
            Row(
                Column('cidade', css_class='form-group col-md-6'),
                Column('estado', css_class='form-group col-md-2'),
                Column('cep', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            'logo',
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )

