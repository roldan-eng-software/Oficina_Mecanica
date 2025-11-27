# Busca de CEP Automática

## 📝 Sobre

Sistema de integração automática com a API pública **ViaCEP** para buscar dados de endereço a partir do CEP. Funcionalidade adicionada a todos os formulários de cadastro que contêm campos de endereço.

## 🎯 Funcionalidades

- ✅ Busca automática de endereço quando CEP é preenchido
- ✅ Preenchimento automático de: Rua, Bairro, Cidade e Estado
- ✅ Validação de CEP (formato: 00000-000 ou 00000000)
- ✅ Mensagens de sucesso/erro ao usuário
- ✅ Integração sem reload de página (AJAX)
- ✅ Funciona em todos os formulários de cadastro

## 🔌 API

### Endpoint

```
GET /api/buscar-cep/?cep=01310100
```

### Resposta de Sucesso (200)

```json
{
    "success": true,
    "data": {
        "rua": "Avenida Paulista",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01310-100"
    }
}
```

### Resposta de Erro (404)

```json
{
    "success": false,
    "error": "CEP não encontrado ou inválido"
}
```

## 🛠️ Implementação Técnica

### Backend

- **Arquivo**: `core/services.py`
- **Classe**: `CEPService`
- **Método**: `buscar_endereco(cep: str) -> Optional[Dict]`

```python
from core.services import CEPService

resultado = CEPService.buscar_endereco('01310100')
# Retorna: {
#     'rua': 'Avenida Paulista',
#     'bairro': 'Bela Vista',
#     'cidade': 'São Paulo',
#     'estado': 'SP',
#     'cep': '01310-100'
# }
```

### Frontend

- **Arquivo**: `core/static/js/cep-lookup.js`
- **Funcionalidade**: Detecta campos de CEP e integra busca automática
- **Eventos**: 
  - `blur` (quando sai do campo CEP)
  - `keypress` (Enter para buscar)

### Páginas Funcionais

- Cadastro de Cliente (`clientes/cliente_form.html`)
- Cadastro de Empresa (`core/` - Empresa)

## 📋 Campos Preenchidos Automaticamente

| Campo | Preenchido | Descrição |
|-------|-----------|-----------|
| `endereco` | ✅ | Rua/Logradouro |
| `bairro` | ✅ | Bairro |
| `cidade` | ✅ | Cidade/Município |
| `estado` | ✅ | Estado/UF |
| `cep` | ✅ | CEP (formatado) |

## 🧪 Testando

### Teste Rápido (CEP válido - São Paulo)

```bash
curl "http://localhost:8000/api/buscar-cep/?cep=01310100"
```

### Script de Teste

```bash
python test_cep_integration.py
```

## 🌐 Exemplos de CEPs para Teste

| CEP | Cidade | Estado |
|-----|--------|--------|
| 01310-100 | São Paulo | SP |
| 13563-846 | São Carlos | SP |
| 22250-040 | Rio de Janeiro | RJ |
| 30140-071 | Belo Horizonte | MG |

## ⚙️ Requisitos

- `requests==2.31.0` (para requisições HTTP)
- Internet para conectar à API ViaCEP

## 📦 Dependências (requirements.txt)

```
requests==2.31.0
```

Já está incluído no `requirements.txt` do projeto.

## 🚀 Como Usar

1. **Acesse um formulário de cadastro** que possua campo CEP
   - Exemplo: `/clientes/novo/`

2. **Preencha o campo CEP**
   - Formato aceito: `01310-100` ou `01310100`

3. **Pressione Tab ou Enter**
   - A busca será realizada automaticamente

4. **Veja os campos preenchidos**
   - Endereço, bairro, cidade e estado serão preenchidos

5. **Complete os dados se necessário**
   - Alguns campos como número podem precisar ser preenchidos manualmente

## 🔍 Detalhes Técnicos

### Como Funciona

1. Usuário preenche o CEP
2. JavaScript detecta o evento (blur ou Enter)
3. Valida o CEP (8 dígitos)
4. Faz requisição à `/api/buscar-cep/`
5. Backend consulta ViaCEP
6. Retorna dados em JSON
7. JavaScript preenche os campos
8. Mostra mensagem de sucesso/erro

### Tratamento de Erros

- CEP inválido: mostra mensagem de erro
- CEP não encontrado: mostra mensagem "CEP não encontrado"
- Erro de conexão: mostra mensagem "Verifique sua conexão"

### Performance

- Requisição é feita via AJAX (não reload da página)
- Timeout de 5 segundos para requisição à ViaCEP
- Mensagens desaparecem automaticamente após 5 segundos

## 📚 Referências

- **API ViaCEP**: https://viacep.com.br/
- **Documentação**: https://viacep.com.br/#/docs

## ⚠️ Limitações

- Funciona apenas online (depende da API ViaCEP)
- ViaCEP pode ter limites de requisições
- CEPs internacionais não são suportados (apenas Brasil)

## 🐛 Troubleshooting

### "CEP não encontrado"
- Verifique se o CEP é válido
- Confirme que tem 8 dígitos

### "Erro ao buscar CEP. Verifique sua conexão"
- Verifique sua conexão com a internet
- Confirme que ViaCEP está acessível

### Campos não preenchem automaticamente
- Verifique se JavaScript está ativado
- Abra o console do navegador (F12) e procure por erros
- Confirme que os nomes dos campos coincidem com os esperados

## 📝 Notas

- A busca é **totalmente opcional**
- Você pode ainda preencher os campos manualmente
- Dados são armazenados no banco de dados após o formulário ser salvo

