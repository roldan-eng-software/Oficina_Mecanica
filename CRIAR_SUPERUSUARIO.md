# 🔐 Como Criar Superusuário no Render

Como o shell do Render requer assinatura paga, aqui estão **3 maneiras** de criar o superusuário:

## Opção 1: Via Variáveis de Ambiente (Recomendado) ⭐

Esta é a forma mais segura e automática. O comando será executado automaticamente durante o build.

### Passos:

1. No dashboard do Render, vá em **Environment** do seu serviço web
2. Adicione as seguintes variáveis de ambiente:

```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=sua-senha-segura-aqui
```

3. Faça um novo deploy (ou aguarde o próximo deploy automático)
4. O superusuário será criado automaticamente durante o build

**Vantagens:**
- Automático
- Seguro (senha não fica no código)
- Funciona a cada deploy (mas só cria se não existir)

## Opção 2: Via Interface Web (Temporária) 🌐

Uma view temporária foi criada para criar o superusuário via navegador.

### Passos:

1. Acesse a URL:
   ```
   https://seu-app.onrender.com/create-superuser/?key=temporary-key-change-me
   ```

2. Preencha o formulário:
   - **Username:** admin (ou o que preferir)
   - **Email:** seu-email@example.com
   - **Senha:** escolha uma senha segura

3. Clique em "Criar Superusuário"

4. **IMPORTANTE:** Após criar o superusuário, remova esta view por segurança:
   - Remova a URL de `core/urls.py`
   - Remova a view de `core/views.py`
   - Remova o template `core/templates/core/create_superuser.html`

**Segurança:**
- A view só funciona se não houver superusuário
- Requer uma chave de acesso (configure `CREATE_SUPERUSER_KEY` no Render para mudar)
- Após criar, a view se desabilita automaticamente

### Mudar a Chave de Acesso:

No Render, adicione a variável de ambiente:
```
CREATE_SUPERUSER_KEY=sua-chave-secreta-personalizada
```

## Opção 3: Via Comando de Gerenciamento (Se tiver acesso)

Se conseguir acesso ao shell ou terminal do Render:

```bash
python manage.py create_superuser_if_not_exists --username admin --email admin@example.com --password sua-senha
```

Ou usando variáveis de ambiente:
```bash
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=sua-senha
python manage.py create_superuser_if_not_exists
```

## 🔒 Segurança

**Após criar o superusuário:**

1. Faça login no `/admin`
2. **IMPORTANTE:** Altere a senha padrão
3. Se usou a Opção 2 (view web), remova a view temporária
4. Configure `DJANGO_SUPERUSER_PASSWORD` nas variáveis de ambiente para futuros deploys

## 📝 Notas

- O comando `create_superuser_if_not_exists` só cria se não existir superusuário
- Se já existir um superusuário, o comando será ignorado
- A senha padrão do comando é `admin123` se não for especificada (NÃO RECOMENDADO para produção)

## ✅ Recomendação

**Use a Opção 1** (Variáveis de Ambiente) - é a mais segura e automática!

