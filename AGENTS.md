# Guia de Padrões e Convenções - Oficina Mecânica

Este documento descreve os padrões de código, estrutura e convenções utilizados no projeto.

## 📋 Padrões Python

### PEP 8
- Seguir rigorosamente o PEP 8 para estilo de código
- Usar 4 espaços para indentação (não tabs)
- Limite de 79 caracteres por linha (quando possível)
- Usar snake_case para nomes de variáveis e funções
- Usar PascalCase para nomes de classes

### Type Hints em Docstrings
Todas as funções e métodos devem ter docstrings descritivas:

```python
def calcular_valor_total(self):
    """
    Calcula o valor total do serviço incluindo peças e mão de obra.
    
    Returns:
        Decimal: Valor total calculado
    """
    pass
```

### Docstrings Descritivas
- Todas as classes devem ter docstrings explicando seu propósito
- Documentar parâmetros, retornos e exceções
- Incluir exemplos quando apropriado

## 🏗️ Estrutura Django

### Apps Separados por Domínio
Cada app representa um domínio de negócio específico:
- `core`: Funcionalidades base e compartilhadas
- `clientes`: Gestão de clientes
- `veiculos`: Gestão de veículos
- `agendamentos`: Agendamento de serviços
- `servicos`: Execução e controle de serviços
- `estoque`: Controle de estoque de peças
- `financeiro`: Gestão financeira

### Convenções de Modelo

#### Herdar BaseModel
Sempre que possível, modelos devem herdar de `BaseModel`:

```python
from core.models import BaseModel

class MeuModelo(BaseModel):
    # Campos específicos
    pass
```

#### Campos Comuns
- `created_at`: Data de criação (auto_now_add=True)
- `updated_at`: Data de atualização (auto_now=True)
- `ativo`: Campo booleano para soft delete (default=True)

#### Nomenclatura
- Nomes de modelos em singular e PascalCase
- Nomes de campos em snake_case
- Usar `verbose_name` e `verbose_name_plural` no Meta

#### Relacionamentos
- Usar `related_name` explícito em ForeignKey
- Preferir `on_delete=models.CASCADE` para dependências fortes
- Usar `on_delete=models.SET_NULL` quando apropriado

### Convenções de View

#### Sempre Usar Class-Based Views
Preferir CBVs sobre function-based views:

```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class MinhaListView(LoginRequiredMixin, ListView):
    model = MeuModelo
    template_name = 'app/minha_list.html'
    context_object_name = 'objetos'
```

#### Mixins de Autenticação
- Sempre usar `LoginRequiredMixin` para views que requerem autenticação
- Usar `PermissionRequiredMixin` quando necessário

#### Nomenclatura de Views
- `ListView`: `ModeloListView`
- `DetailView`: `ModeloDetailView`
- `CreateView`: `ModeloCreateView`
- `UpdateView`: `ModeloUpdateView`
- `DeleteView`: `ModeloDeleteView`

### Padrões de Formulário

#### Usar django-crispy-forms
Todos os formulários devem usar crispy_forms:

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class MeuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Campos aqui
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )
```

#### Validação
- Validação básica nos modelos (validators)
- Validação customizada nos forms (clean_*)
- Validação de negócio nas views quando necessário

### Padrões de Template

#### Usar crispy_forms_tags
Sempre carregar e usar crispy_forms nos templates:

```django
{% load crispy_forms_tags %}
{% crispy form %}
```

#### Estrutura de Templates
- `base.html`: Template base com navbar e footer
- `app/modelo_list.html`: Listagem
- `app/modelo_detail.html`: Detalhes
- `app/modelo_form.html`: Formulário (criar/editar)
- `app/modelo_confirm_delete.html`: Confirmação de exclusão

#### Bootstrap 5
- Usar classes Bootstrap 5 para layout
- Manter responsividade
- Usar ícones Bootstrap Icons

### Padrões de URL

#### Namespace e app_name
Sempre definir `app_name` em `urls.py`:

```python
app_name = 'meu_app'

urlpatterns = [
    path('', MinhaListView.as_view(), name='minha_list'),
]
```

#### Nomenclatura RESTful
- Lista: `app/modelos/` → `modelo_list`
- Detalhe: `app/modelos/<int:pk>/` → `modelo_detail`
- Criar: `app/modelos/novo/` → `modelo_create`
- Editar: `app/modelos/<int:pk>/editar/` → `modelo_update`
- Excluir: `app/modelos/<int:pk>/excluir/` → `modelo_delete`

#### Incluir URLs no config/urls.py
```python
path('meu_app/', include('meu_app.urls')),
```

## 🛡️ Tratamento de Erros

### Usar Messages Framework
Sempre usar o sistema de mensagens do Django:

```python
from django.contrib import messages

def minha_view(request):
    if sucesso:
        messages.success(request, 'Operação realizada com sucesso!')
    else:
        messages.error(request, 'Erro ao realizar operação.')
```

### Validação de Dados

#### Em Models
```python
from django.core.validators import MinValueValidator, RegexValidator

valor = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.00'))]
)
```

#### Em Forms
```python
def clean_campo(self):
    campo = self.cleaned_data.get('campo')
    if not campo:
        raise forms.ValidationError('Campo é obrigatório.')
    return campo
```

#### Em Views
```python
try:
    objeto = MeuModelo.objects.get(pk=pk)
except MeuModelo.DoesNotExist:
    messages.error(request, 'Objeto não encontrado.')
    return redirect('app:lista')
```

## 🎨 Padrões de Template

### Bootstrap 5
- Validar uso correto de classes Bootstrap 5
- Manter consistência visual
- Usar componentes Bootstrap (cards, tables, forms)

### Acessibilidade
- Usar labels apropriados
- Manter contraste adequado
- Usar atributos ARIA quando necessário
- Estrutura semântica HTML

### Responsividade
- Usar grid system do Bootstrap
- Testar em diferentes tamanhos de tela
- Mobile-first quando possível

## 📁 Estrutura de Arquivos

### Organização
```
app/
├── __init__.py
├── admin.py          # Configuração do admin
├── apps.py          # Configuração do app
├── models.py        # Modelos
├── views.py         # Views
├── urls.py          # URLs
├── forms.py         # Formulários
├── templates/       # Templates
│   └── app/
│       ├── modelo_list.html
│       ├── modelo_detail.html
│       ├── modelo_form.html
│       └── modelo_confirm_delete.html
└── static/          # Arquivos estáticos (se necessário)
    ├── css/
    └── js/
```

## 🔒 Segurança

### Autenticação
- Sempre usar `@login_required` ou `LoginRequiredMixin`
- Validar permissões quando necessário
- Não expor dados sensíveis em templates

### CSRF Protection
- Django já protege automaticamente
- Sempre usar `{% csrf_token %}` em forms

### SQL Injection
- Sempre usar ORM do Django
- Nunca construir queries SQL manualmente com strings

## 📝 Convenções de Código

### Imports
Ordem de imports:
1. Bibliotecas padrão
2. Bibliotecas de terceiros
3. Imports do Django
4. Imports locais

```python
# 1. Standard library
from datetime import datetime

# 2. Third-party
from crispy_forms.helper import FormHelper

# 3. Django
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin

# 4. Local
from core.models import BaseModel
```

### Nomes de Variáveis
- `objeto`: Instância de modelo
- `objetos`: QuerySet ou lista
- `form`: Formulário
- `context`: Contexto de template

## 🧪 Testes (Futuro)

Quando implementar testes:
- Usar `django.test.TestCase`
- Testar models, views, forms
- Manter cobertura acima de 80%

## 📚 Documentação

### Docstrings
- Todas as classes e métodos públicos devem ter docstrings
- Usar formato Google ou NumPy style

### Comentários
- Comentar código complexo
- Evitar comentários óbvios
- Manter comentários atualizados

## 🔄 Versionamento

- Usar Git para controle de versão
- Commits descritivos
- Branches para features
- Pull requests para revisão

## 📦 Dependências

- Manter `requirements.txt` atualizado
- Especificar versões exatas
- Documentar dependências opcionais

## 🚀 Performance

### Queries
- Usar `select_related()` para ForeignKey
- Usar `prefetch_related()` para ManyToMany
- Evitar N+1 queries

### Paginação
- Sempre paginar listagens grandes
- Usar `paginate_by` nas ListViews

### Cache (Futuro)
- Considerar cache para queries frequentes
- Cache de templates quando apropriado

