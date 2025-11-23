# Sistema de Gestão de Oficina Mecânica

Sistema completo de gestão para oficinas mecânicas de automóveis desenvolvido em Django.

## 📋 Descrição

Este sistema permite gerenciar todos os aspectos de uma oficina mecânica, incluindo:
- Cadastro de clientes e veículos
- Agendamento de serviços
- Controle de serviços e orçamentos
- Gestão de estoque de peças
- Controle financeiro (contas a receber e a pagar)
- Dashboard com estatísticas gerais

## 🛠️ Tecnologias Utilizadas

- **Django 4.2.7** - Framework web Python
- **Bootstrap 5** - Framework CSS
- **django-crispy-forms** - Formulários estilizados
- **Pillow** - Processamento de imagens
- **SQLite** - Banco de dados (desenvolvimento)
- **PostgreSQL** - Banco de dados (produção, configurável)

## 📦 Requisitos do Sistema

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Virtual environment (recomendado)

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd Oficina_Mecanica
```

### 2. Criar e Ativar Ambiente Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar Migrações

```bash
python manage.py migrate
```

### 5. Criar Superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções para criar um usuário administrador.

### 6. Coletar Arquivos Estáticos (se necessário)

```bash
python manage.py collectstatic --noinput
```

### 7. Executar o Servidor

```bash
python manage.py runserver
```

O sistema estará disponível em: `http://localhost:8000`

## 📱 Acesso ao Sistema

- **Interface Principal:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin

## 📚 Estrutura de Módulos

### Core
- Modelos base (BaseModel, Empresa, Usuario)
- Dashboard principal com estatísticas

### Clientes
- Cadastro completo de clientes
- Busca e filtros
- Histórico de veículos

### Veículos
- Cadastro de veículos por cliente
- Status de manutenção
- Histórico de serviços

### Agendamentos
- Agendamento de serviços
- Atribuição de mecânicos
- Calendário de agendamentos
- Alertas de agendamentos próximos

### Serviços
- Criação e gestão de serviços
- Orçamentos detalhados
- Controle de status
- Cálculo automático de valores

### Estoque
- Cadastro de peças
- Controle de estoque mínimo
- Movimentações (entrada/saída)
- Alertas de estoque baixo

### Financeiro
- Contas a receber
- Contas a pagar
- Dashboard financeiro
- Relatórios (em desenvolvimento)

## 👥 Estrutura de Usuários e Permissões

O sistema possui diferentes níveis de acesso:

- **Administrador:** Acesso total ao sistema
- **Gerente:** Acesso a todas as funcionalidades operacionais
- **Mecânico:** Acesso a agendamentos e serviços
- **Atendente:** Acesso básico para cadastros e consultas

## 🔄 Fluxos de Trabalho Principais

### 1. Cadastro de Cliente e Veículo
1. Acesse "Clientes" → "Novo Cliente"
2. Preencha os dados do cliente
3. Acesse "Veículos" → "Novo Veículo"
4. Associe o veículo ao cliente

### 2. Agendamento de Serviço
1. Acesse "Agendamentos" → "Novo Agendamento"
2. Selecione o veículo e cliente
3. Defina data/hora e mecânico responsável
4. Adicione descrição do problema

### 3. Execução de Serviço
1. Acesse o agendamento e crie um serviço
2. Adicione itens ao orçamento (peças e serviços)
3. Defina preço de mão de obra
4. Atualize status conforme progresso

### 4. Controle de Estoque
1. Cadastre peças em "Estoque"
2. Defina quantidade mínima
3. Registre movimentações (entrada/saída)
4. Monitore alertas de estoque baixo

### 5. Gestão Financeira
1. Contas a receber são criadas automaticamente ao finalizar serviços
2. Registre pagamentos recebidos
3. Cadastre contas a pagar (fornecedores, despesas)
4. Monitore dashboard financeiro

## 📊 Relatórios

### Dashboard Principal
- Total de clientes e veículos
- Agendamentos do dia
- Serviços em progresso
- Estoque baixo
- Contas vencidas

### Dashboard Financeiro
- Total a receber/pagar
- Recebimentos/pagamentos do mês
- Saldo mensal
- Alertas de contas vencidas

## 🔧 Configuração para Produção

### Banco de Dados PostgreSQL

Edite `config/settings.py` e descomente a configuração do PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oficina_mecanica',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Variáveis de Ambiente

Crie um arquivo `.env` para variáveis sensíveis:

```
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

### Configurações de Segurança

- Altere `SECRET_KEY` em produção
- Configure `ALLOWED_HOSTS` adequadamente
- Defina `DEBUG=False` em produção
- Configure HTTPS

## 🐛 Solução de Problemas

### Erro ao executar migrações
Certifique-se de que todas as dependências estão instaladas:
```bash
pip install -r requirements.txt
```

### Erro de permissões
Verifique se o usuário tem permissões adequadas no banco de dados.

### Arquivos estáticos não carregam
Execute:
```bash
python manage.py collectstatic
```

## 📝 Licença

Este projeto é de uso livre para fins educacionais e comerciais.

## 👨‍💻 Desenvolvimento

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório do projeto.

