#!/usr/bin/env bash
# Build script para Render.com

set -o errexit  # Exit on error

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Executando migrações..."
python manage.py migrate --noinput

echo "Build concluído!"

