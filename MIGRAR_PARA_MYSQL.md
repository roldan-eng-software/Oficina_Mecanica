# Migração para MySQL

Este arquivo descreve os passos para migrar o projeto `Oficina_Mecanica` de SQLite/Postgres para MySQL.

Resumo das alterações efetuadas automaticamente pelo assistente:
- Adicionado `PyMySQL` em `requirements.txt`.
- Registrado `pymysql.install_as_MySQLdb()` em `config/__init__.py` para permitir uso do driver PyMySQL.
- `config/settings.py` foi atualizado para reconhecer `DATABASE_URL` com esquema `mysql://` ou `mysql+pymysql://`.

Passos recomendados para migrar (local ou produção):

1) Instale dependências no virtualenv

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

2) Prepare o servidor MySQL e crie o banco de dados
- Crie um database e um usuário com privilégios adequados.
- Configure `utf8mb4` e collation compatível (recomendado `utf8mb4_unicode_ci`).

Exemplo (MySQL root):

```sql
CREATE DATABASE oficina CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'oficina_user'@'%' IDENTIFIED BY 'senha-segura';
GRANT ALL PRIVILEGES ON oficina.* TO 'oficina_user'@'%';
FLUSH PRIVILEGES;
```

3) Defina `DATABASE_URL` ou variáveis equivalentes no ambiente
- `DATABASE_URL` no formato: `mysql://user:password@host:3306/dbname`
- Ou defina variáveis individuais e adapte `config/settings.py` se desejar.

Exemplo PowerShell:

```powershell
$env:DATABASE_URL = 'mysql://oficina_user:senha-segura@db-host:3306/oficina'
$env:DEBUG = 'False'
$env:SECRET_KEY = 'uma-chave-muito-longa-e-segura-de-50-ou-mais-caracteres'
```

4) Fazer dump dos dados atuais (opcional) e migrar
- Se estiver migrando dados do SQLite/Postgres para MySQL, use `dumpdata`/`loaddata` ou exporte via ferramentas específicas.

Exemplo usando `dumpdata` (atenção: dados grandes podem precisar de abordagem diferente):

```powershell
.venv\Scripts\python.exe manage.py dumpdata --natural-primary --natural-foreign --indent 2 > dump.json
# Mude DATABASE_URL para apontar para MySQL
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py loaddata dump.json
```

Observações importantes:
- `dumpdata` / `loaddata` podem não preservar perfeitamente tipos binários, estados de PK/autoincrement, ou dados complexos; para bases grandes prefira `mysqldump`/`pg_dump` com scripts de transformação.
- Para grandes volumes de dados, use ferramentas ETL ou scripts personalizados.

5) Rodar migrações no MySQL

```powershell
.venv\Scripts\python.exe manage.py migrate
```

6) Verificar integridade e testar manualmente a aplicação
- Acesse a aplicação, execute fluxos principais (cadastro de clientes, agendamentos, serviços, etc.) e verifique logs de erro.

7) Ajustes finos
- Configure variáveis de ambiente de produção (HSTS, SSL redirect, cookies seguros, etc.) em `config/settings.py` conforme já instruído.

Se quiser, posso:
- Tentar rodar `pip install` aqui no `.venv` (já adicionei `PyMySQL` ao `requirements.txt`).
- Ajudar a executar `dumpdata`/`migrate`/`loaddata` se você fornecer acesso ao servidor MySQL ou as credenciais (defina em variáveis de ambiente no seu ambiente seguro).
- Fornecer um script automatizado para migrar dados grandes.

