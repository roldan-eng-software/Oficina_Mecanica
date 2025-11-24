"""
Serviços compartilhados para o projeto.
"""
import requests
from typing import Optional, Dict


class CEPService:
    """
    Serviço para buscar dados de endereço via CEP.
    Utiliza a API pública ViaCEP.
    """
    
    BASE_URL = "https://viacep.com.br/ws"
    TIMEOUT = 5  # segundos
    
    @staticmethod
    def buscar_endereco(cep: str) -> Optional[Dict]:
        """
        Busca informações de endereço a partir de um CEP.
        
        Args:
            cep: CEP no formato com ou sem máscara (00000-000 ou 00000000)
            
        Returns:
            Dict com chaves: rua, numero, complemento, bairro, cidade, estado
            Retorna None se CEP não for encontrado ou houver erro.
        """
        if not cep:
            return None
        
        # Remove máscara do CEP
        cep_limpo = cep.replace('-', '').replace('.', '').strip()
        
        # Valida se tem 8 dígitos
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            return None
        
        try:
            # Faz requisição à API ViaCEP
            url = f"{CEPService.BASE_URL}/{cep_limpo}/json/"
            response = requests.get(url, timeout=CEPService.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Verifica se não foi encontrado
            if data.get('erro'):
                return None
            
            # Retorna dados formatados
            return {
                'rua': data.get('logradouro', ''),
                'bairro': data.get('bairro', ''),
                'cidade': data.get('localidade', ''),
                'estado': data.get('uf', ''),
                'cep': f"{cep_limpo[:5]}-{cep_limpo[5:]}",  # Formata CEP
            }
        
        except requests.RequestException:
            # Se houver erro de conexão, retorna None
            return None
        except (ValueError, KeyError):
            # Se JSON estiver inválido, retorna None
            return None
