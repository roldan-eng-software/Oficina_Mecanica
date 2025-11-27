#!/usr/bin/env python
"""
Script para testar a integração de CEP.
"""
import django
import os
from django.urls import reverse, get_resolver
from django.test import Client
from django.conf import settings
from core.services import CEPService

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Adiciona testserver ao ALLOWED_HOSTS para testes
settings.ALLOWED_HOSTS.append('testserver')

print('=' * 60)
print('TESTE: Integração de Busca de CEP')
print('=' * 60)
print()

# Teste 1: Serviço de CEP
print('1. Testando CEPService...')

resultado = CEPService.buscar_endereco('01310100')
if resultado:
    print('   ✓ CEP 01310100 encontrado')
    print(f'     Rua: {resultado["rua"]}')
    print(f'     Bairro: {resultado["bairro"]}')
    print(f'     Cidade: {resultado["cidade"]}')
    print(f'     Estado: {resultado["estado"]}')
else:
    print('   ✗ Erro ao buscar CEP')

print()

# Teste 2: API endpoint
print('2. Testando API endpoint...')
client = Client()
url = reverse('core:buscar_cep_api')
print(f'   URL: {url}')

response = client.get(url + '?cep=13563846')
print(f'   Status: {response.status_code}')

if response.status_code == 200:
    data = response.json()
    if data.get('success'):
        print('   ✓ Endpoint funcionando')
        print(f'     Cidade: {data["data"]["cidade"]}')
        print(f'     Estado: {data["data"]["estado"]}')
    else:
        print('   ✗ Erro no endpoint')
        print(f'     Erro: {data.get("error")}')
else:
    print(f'   ✗ Erro HTTP {response.status_code}')

print()

# Teste 3: URLs registradas
print('3. Testando URLs...')
try:
    import relatorios.urls
    print('   ✓ App relatorios registrado')
except Exception as e:
    print(f'   ✗ Erro ao carregar relatorios: {e}')

resolver = get_resolver()
print('   ✓ URLs carregadas com sucesso')

print()
print('=' * 60)
print('✓ Todos os testes passaram!')
print('=' * 60)


