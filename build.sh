#!/usr/bin/env bash
# Build script para Render.com

set -o errexit  # Exit on error

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Executando migrações..."
python manage.py migrate --noinput

echo "Criando superusuário se não existir..."
python manage.py create_superuser_if_not_exists

echo "Build concluído!"
echo ""
echo "Para resetar senha do admin, use:"
echo "  - Via web: /reset-superuser/?key=temporary-key-change-me"
echo "  - Ou configure DJANGO_SUPERUSER_PASSWORD nas variáveis de ambiente e faça redeploy"

