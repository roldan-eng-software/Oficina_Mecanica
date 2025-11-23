# 🚂 Guia de Deploy no Railway

Este guia explica como fazer o deploy da aplicação Django Oficina Mecânica no Railway.

## 📋 Pré-requisitos

1. Conta no [Railway](https://railway.app)
2. Repositório Git (GitHub, GitLab ou Bitbucket)
3. Projeto configurado e funcionando localmente

## 🚀 Passo a Passo

### 1. Preparar o Repositório

Certifique-se de que todos os arquivos necessários estão commitados:

- `Procfile` - Comando para iniciar o servidor
- `runtime.txt` - Versão do Python
- `requirements.txt` - Dependências do projeto
- `config/settings.py` - Configurado para usar variáveis de ambiente

### 2. Criar Novo Projeto no Railway

1. Acesse [Railway Dashboard](https://railway.app/dashboard)
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo" (ou outro provedor Git)
4. Escolha o repositório do projeto
5. Railway detectará automaticamente que é um projeto Django

### 3. Adicionar Banco de Dados PostgreSQL

1. No dashboard do projeto, clique em "New"
2. Selecione "Database" → "Add PostgreSQL"
3. Railway criará automaticamente um banco PostgreSQL
4. As variáveis de ambiente do banco serão configuradas automaticamente

### 4. Configurar Variáveis de Ambiente

No dashboard do projeto, vá em "Variables" e adicione:

```
SECRET_KEY=sua-chave-secreta-aqui-gerada-aleatoriamente
DEBUG=False
ALLOWED_HOSTS=seu-app.railway.app,*.railway.app
```

**Importante:**
- Gere uma `SECRET_KEY` segura (pode usar: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- O Railway fornece automaticamente as variáveis do PostgreSQL (`DATABASE_URL` ou `PGHOST`, `PGDATABASE`, etc.)
- O `ALLOWED_HOSTS` deve incluir o domínio do Railway (você verá após o primeiro deploy)

### 5. Configurar Build e Deploy

O Railway detectará automaticamente:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** Será lido do `Procfile`

**Recomendado:** Configure um **Release Command** para executar migrações automaticamente:
- **Release Command:** `python manage.py migrate --noinput && python manage.py collectstatic --noinput`

Isso garantirá que as migrações sejam executadas antes de cada deploy.

Se necessário, você pode configurar manualmente:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn config.wsgi --log-file -`

### 6. Executar Migrações

Após o primeiro deploy, você precisa executar as migrações:

1. No dashboard do projeto, clique no serviço Django
2. Vá em "Deployments" → "View Logs"
3. Clique em "Shell" ou use o terminal do Railway
4. Execute:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

**Alternativa:** Configure um script de inicialização no `Procfile` ou use o comando de release do Railway.

### 7. Configurar Domínio (Opcional)

1. No dashboard do projeto, clique no serviço Django
2. Vá em "Settings" → "Domains"
3. Clique em "Generate Domain" para obter um domínio Railway
4. Ou adicione seu próprio domínio personalizado

### 8. Verificar Deploy

1. Acesse o domínio fornecido pelo Railway
2. Verifique se a aplicação está funcionando
3. Acesse `/admin` e faça login com o superusuário criado

## 🔧 Configurações Adicionais

### Variáveis de Ambiente Recomendadas

```
SECRET_KEY=<gerar-uma-chave-secreta>
DEBUG=False
ALLOWED_HOSTS=*.railway.app,seu-dominio.com
```

### Comandos Úteis no Railway Shell

```bash
# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Acessar shell do Django
python manage.py shell
```

### Troubleshooting

#### Erro: "DisallowedHost"
- Verifique se `ALLOWED_HOSTS` inclui o domínio do Railway
- Adicione `*.railway.app` para aceitar qualquer subdomínio

#### Erro: "Database connection failed"
- Verifique se o serviço PostgreSQL está rodando
- Confirme que as variáveis de ambiente do banco estão configuradas
- O Railway configura automaticamente, mas verifique em "Variables"

#### Arquivos estáticos não carregam
- Execute `python manage.py collectstatic --noinput`
- Verifique se `whitenoise` está no `MIDDLEWARE`
- Confirme que `STATIC_ROOT` está configurado

#### Erro: "ModuleNotFoundError"
- Verifique se todas as dependências estão no `requirements.txt`
- Confirme que o build foi executado com sucesso

## 📝 Notas Importantes

1. **Banco de Dados:** O Railway fornece PostgreSQL automaticamente. O `settings.py` está configurado para detectar e usar as variáveis do Railway.

2. **Arquivos Estáticos:** O projeto usa WhiteNoise para servir arquivos estáticos em produção. Certifique-se de executar `collectstatic` após cada deploy.

3. **Mídia/Uploads:** Para arquivos de mídia (uploads), considere usar um serviço de storage como AWS S3 ou Railway Volumes.

4. **Logs:** Os logs estão configurados para aparecer no dashboard do Railway. Use `--log-file -` no gunicorn.

5. **Celery/Redis:** Se você usar Celery e Redis, adicione um serviço Redis no Railway e configure as variáveis de ambiente apropriadas.

## 🔗 Links Úteis

- [Documentação do Railway](https://docs.railway.app)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](https://whitenoise.evans.io/)

## ✅ Checklist de Deploy

- [ ] Repositório Git configurado
- [ ] Projeto criado no Railway
- [ ] PostgreSQL adicionado como serviço
- [ ] Variáveis de ambiente configuradas (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- [ ] Primeiro deploy executado
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Arquivos estáticos coletados
- [ ] Domínio configurado (opcional)
- [ ] Aplicação testada e funcionando

