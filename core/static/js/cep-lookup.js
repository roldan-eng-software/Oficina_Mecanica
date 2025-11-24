/**
 * Script para integração de busca de CEP automática em formulários.
 * Busca endereço via API ViaCEP quando o campo CEP é preenchido.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Encontra campos de CEP no formulário
    const cepInputs = document.querySelectorAll('input[name="cep"]');
    
    cepInputs.forEach(function(cepInput) {
        // Adiciona listener para evento de blur (quando sai do campo)
        cepInput.addEventListener('blur', function() {
            const cep = this.value.trim();
            
            // Valida se CEP tem 8+ dígitos (com ou sem máscara)
            const cepDigitos = cep.replace(/\D/g, '');
            if (cepDigitos.length < 8) {
                return; // Ignora CEPs incompletos
            }
            
            // Busca endereço via API
            buscarEndereco(cep);
        });
        
        // Permite buscar ao pressionar Enter
        cepInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const cep = this.value.trim();
                const cepDigitos = cep.replace(/\D/g, '');
                if (cepDigitos.length >= 8) {
                    buscarEndereco(cep);
                }
            }
        });
    });
});

/**
 * Busca endereço por CEP e preenche os campos do formulário.
 * @param {string} cep - CEP para buscar
 */
function buscarEndereco(cep) {
    const url = '/api/buscar-cep/?cep=' + encodeURIComponent(cep);
    
    // Feedback visual
    mostrarCarregando(true);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            mostrarCarregando(false);
            
            if (data.success) {
                preencherFormulario(data.data);
                mostrarMensagem('Endereço encontrado com sucesso!', 'success');
            } else {
                mostrarMensagem(data.error || 'CEP não encontrado.', 'error');
            }
        })
        .catch(error => {
            mostrarCarregando(false);
            console.error('Erro ao buscar CEP:', error);
            mostrarMensagem('Erro ao buscar CEP. Verifique sua conexão.', 'error');
        });
}

/**
 * Preenche os campos de endereço no formulário.
 * @param {object} endereco - Objeto com dados de endereço
 */
function preencherFormulario(endereco) {
    // Encontra os campos no formulário
    const form = document.querySelector('form');
    if (!form) return;
    
    // Tenta preencher rua/logradouro
    const ruaInput = form.querySelector('input[name="endereco"]');
    if (ruaInput && endereco.rua) {
        ruaInput.value = endereco.rua;
    }
    
    // Tenta preencher bairro
    const bairroInputs = [
        form.querySelector('input[name="bairro"]'),
        form.querySelector('input[name="neighborhood"]'),
        form.querySelector('input[name="district"]')
    ];
    bairroInputs.forEach(input => {
        if (input && endereco.bairro) {
            input.value = endereco.bairro;
        }
    });
    
    // Tenta preencher cidade
    const cidadeInputs = [
        form.querySelector('input[name="cidade"]'),
        form.querySelector('input[name="city"]')
    ];
    cidadeInputs.forEach(input => {
        if (input && endereco.cidade) {
            input.value = endereco.cidade;
        }
    });
    
    // Tenta preencher estado/UF
    const estadoInputs = [
        form.querySelector('input[name="estado"]'),
        form.querySelector('select[name="estado"]'),
        form.querySelector('input[name="state"]'),
        form.querySelector('select[name="state"]')
    ];
    estadoInputs.forEach(input => {
        if (input && endereco.estado) {
            if (input.tagName === 'SELECT') {
                // Para select, procura a opção com o valor
                const option = Array.from(input.options).find(opt => 
                    opt.value === endereco.estado || opt.text === endereco.estado
                );
                if (option) {
                    input.value = option.value;
                }
            } else {
                // Para input, apenas preenche o valor
                input.value = endereco.estado;
            }
        }
    });
    
    // Atualiza CEP com formatação
    const cepInput = form.querySelector('input[name="cep"]');
    if (cepInput && endereco.cep) {
        cepInput.value = endereco.cep;
    }
    
    // Trigger change events para validação de formulários
    form.querySelectorAll('input, select').forEach(field => {
        field.dispatchEvent(new Event('change', { bubbles: true }));
    });
}

/**
 * Mostra/oculta indicador de carregamento.
 * @param {boolean} mostrar - True para mostrar, False para ocultar
 */
function mostrarCarregando(mostrar) {
    const form = document.querySelector('form');
    if (!form) return;
    
    let loader = form.querySelector('.cep-loader');
    
    if (mostrar) {
        if (!loader) {
            loader = document.createElement('div');
            loader.className = 'cep-loader';
            loader.innerHTML = '<small class="text-muted"><i class="bi bi-hourglass-split"></i> Buscando CEP...</small>';
            const cepInput = form.querySelector('input[name="cep"]');
            if (cepInput) {
                cepInput.parentNode.appendChild(loader);
            }
        }
        loader.style.display = 'block';
    } else {
        if (loader) {
            loader.style.display = 'none';
        }
    }
}

/**
 * Mostra mensagem de feedback ao usuário.
 * @param {string} mensagem - Texto da mensagem
 * @param {string} tipo - 'success', 'error', 'warning', 'info'
 */
function mostrarMensagem(mensagem, tipo) {
    const form = document.querySelector('form');
    if (!form) return;
    
    // Remove mensagem anterior se existir
    const msgAnterior = form.querySelector('.cep-message');
    if (msgAnterior) {
        msgAnterior.remove();
    }
    
    // Cria nova mensagem
    const alertClass = tipo === 'success' ? 'alert-success' : 
                      tipo === 'error' ? 'alert-danger' : 
                      tipo === 'warning' ? 'alert-warning' : 'alert-info';
    
    const msgDiv = document.createElement('div');
    msgDiv.className = `alert ${alertClass} alert-dismissible fade show cep-message`;
    msgDiv.setAttribute('role', 'alert');
    msgDiv.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Adiciona antes do primeiro input
    const primeiroInput = form.querySelector('input, textarea, select');
    if (primeiroInput) {
        primeiroInput.parentNode.insertBefore(msgDiv, primeiroInput);
    } else {
        form.insertBefore(msgDiv, form.firstChild);
    }
    
    // Remove automaticamente após 5 segundos
    setTimeout(() => {
        msgDiv.remove();
    }, 5000);
}
