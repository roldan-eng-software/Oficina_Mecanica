# 🚀 Guia de Deploy no Render.com

Este guia explica como fazer o deploy da aplicação Django Oficina Mecânica no Render.com.

## 📋 Pré-requisitos

1. Conta no [Render](https://render.com)
2. Repositório Git (GitHub, GitLab ou Bitbucket)
3. Projeto configurado e funcionando localmente

## 🚀 Passo a Passo

### 1. Preparar o Repositório

Certifique-se de que todos os arquivos necessários estão commitados:

- `Procfile` - Comando para iniciar o servidor
- `build.sh` - Script de build com migrações
- `runtime.txt` - Versão do Python
- `requirements.txt` - Dependências do projeto
- `config/settings.py` - Configurado para usar variáveis de ambiente

### 2. Criar Novo Serviço Web no Render

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório Git
4. Escolha o repositório do projeto

### 3. Configurar o Serviço Web

**Configurações Básicas:**
- **Name:** `oficina-mecanica` (ou o nome que preferir)
- **Region:** Escolha a região mais próxima
- **Branch:** `main` (ou sua branch principal)
- **Root Directory:** Deixe em branco (raiz do projeto)
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh` ou `chmod +x build.sh && ./build.sh`
- **Start Command:** `gunicorn config.wsgi --log-file -`

### 4. Adicionar Banco de Dados PostgreSQL

1. No dashboard do Render, clique em "New +" → "PostgreSQL"
2. Configure:
   - **Name:** `oficina-mecanica-db` (ou o nome que preferir)
   - **Database:** Deixe o padrão ou escolha um nome
   - **User:** Deixe o padrão
   - **Region:** Mesma região do serviço web
3. Clique em "Create Database"
4. **IMPORTANTE:** Anote as credenciais do banco de dados

### 5. Conectar o Banco ao Serviço Web

1. No dashboard do seu serviço web, vá em "Environment"
2. Clique em "Add Environment Variable"
3. Adicione a variável `DATABASE_URL`:
   - **Key:** `DATABASE_URL`
   - **Value:** Copie o "Internal Database URL" do serviço PostgreSQL
   - **Alternativa:** Use o "External Database URL" se necessário

**Formato do DATABASE_URL:**
```
postgresql://usuario:senha@host:porta/database
```

### 6. Configurar Variáveis de Ambiente

No dashboard do serviço web, em "Environment", adicione:

```
SECRET_KEY=sua-chave-secreta-aqui-gerada-aleatoriamente
DEBUG=False
ALLOWED_HOSTS=oficina-mecanica-x07b.onrender.com
```

**Importante:**
- Gere uma `SECRET_KEY` segura:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- O `ALLOWED_HOSTS` deve incluir o domínio do Render (você verá após o primeiro deploy)
- Com a configuração atual, o Django aceita automaticamente domínios `.onrender.com`

### 7. Executar Migrações

O script `build.sh` executa as migrações automaticamente durante o build. Se precisar executar manualmente:

1. No dashboard do serviço, vá em "Shell"
2. Execute:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

### 8. Configurar Domínio

1. No dashboard do serviço web, vá em "Settings" → "Custom Domain"
2. Clique em "Generate Domain" para obter um domínio Render
3. Ou adicione seu próprio domínio personalizado

### 9. Verificar Deploy

1. Acesse o domínio fornecido pelo Render
2. Verifique se a aplicação está funcionando
3. Acesse `/admin` e faça login com o superusuário criado

## 🔧 Configurações Adicionais

### Variáveis de Ambiente Recomendadas

```
SECRET_KEY=<gerar-uma-chave-secreta>
DEBUG=False
ALLOWED_HOSTS=*.onrender.com,seu-dominio.com
DATABASE_URL=<fornecido-automaticamente-pelo-render>
```

### Comandos Úteis no Render Shell

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
- Verifique se `ALLOWED_HOSTS` inclui o domínio do Render
- Com a configuração atual, domínios `.onrender.com` são aceitos automaticamente

#### Erro: "no such table: auth_user"
- **Causa:** Migrações não foram executadas ou banco não está configurado
- **Solução:**
  1. Verifique se o PostgreSQL foi adicionado como serviço
  2. Verifique se `DATABASE_URL` está configurada nas variáveis de ambiente
  3. Execute as migrações manualmente via Shell ou aguarde o build.sh executar

#### Erro: "Database connection failed"
- Verifique se o serviço PostgreSQL está rodando
- Confirme que `DATABASE_URL` está configurada corretamente
- Use o "Internal Database URL" para melhor performance

#### Arquivos estáticos não carregam
- O `build.sh` executa `collectstatic` automaticamente
- Verifique se `whitenoise` está no `MIDDLEWARE`
- Confirme que `STATIC_ROOT` está configurado

#### Erro: "ModuleNotFoundError"
- Verifique se todas as dependências estão no `requirements.txt`
- Confirme que o build foi executado com sucesso

## 📝 Notas Importantes

1. **Banco de Dados:** O Render fornece PostgreSQL. Certifique-se de adicionar o serviço PostgreSQL e conectar via `DATABASE_URL`.

2. **Arquivos Estáticos:** O projeto usa WhiteNoise para servir arquivos estáticos em produção. O `build.sh` executa `collectstatic` automaticamente.

3. **Mídia/Uploads:** Para arquivos de mídia (uploads), considere usar um serviço de storage como AWS S3 ou Render Disk.

4. **Logs:** Os logs estão configurados para aparecer no dashboard do Render. Use `--log-file -` no gunicorn.

5. **Build Script:** O `build.sh` executa automaticamente:
   - Instalação de dependências
   - Coleta de arquivos estáticos
   - Execução de migrações

## 🔗 Links Úteis

- [Documentação do Render](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](https://whitenoise.evans.io/)

## ✅ Checklist de Deploy

- [ ] Repositório Git configurado
- [ ] Serviço Web criado no Render
- [ ] PostgreSQL adicionado como serviço
- [ ] `DATABASE_URL` configurada nas variáveis de ambiente
- [ ] Variáveis de ambiente configuradas (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- [ ] Build Command configurado (`./build.sh`)
- [ ] Start Command configurado (`gunicorn config.wsgi --log-file -`)
- [ ] Primeiro deploy executado
- [ ] Migrações executadas (via build.sh ou manualmente)
- [ ] Superusuário criado
- [ ] Domínio configurado
- [ ] Aplicação testada e funcionando




