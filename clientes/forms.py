"""
Formulários do app clientes.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Cliente


class ClienteForm(forms.ModelForm):
    """Formulário para Cliente."""
    
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf_cnpj', 'email', 'telefone', 'endereco', 
                  'cidade', 'estado', 'cep', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'data-mask': 'cpf'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'data-mask': 'phone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'data-mask': 'cep'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-8'),
                Column('cpf_cnpj', css_class='form-group col-md-4'),
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
            'ativo',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )

    def clean_cpf_cnpj(self):
        """Validação customizada para CPF/CNPJ."""
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        if cpf_cnpj:
            # Remove caracteres não numéricos
            cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj))
            if len(cpf_cnpj) not in [11, 14]:
                raise forms.ValidationError('CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos.')
        return cpf_cnpj

