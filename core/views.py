"""
Views do app core.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q, F
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import os

from clientes.models import Cliente
from veiculos.models import Veiculo
from agendamentos.models import Agendamento
from servicos.models import Servico
from estoque.models import Peca
from financeiro.models import ContaReceber, ContaPagar
from .services import CEPService

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    View para o dashboard principal com estatísticas gerais.
    """
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas gerais
        context['total_clientes'] = Cliente.objects.filter(ativo=True).count()
        context['total_veiculos'] = Veiculo.objects.filter(ativo=True).count()
        
        # Agendamentos
        hoje = datetime.now().date()
        context['agendamentos_hoje'] = Agendamento.objects.filter(
            data_hora__date=hoje,
            status__in=['agendado', 'em_progresso']
        ).count()
        context['agendamentos_proximos'] = Agendamento.objects.filter(
            data_hora__date__gte=hoje,
            data_hora__date__lte=hoje + timedelta(days=7),
            status='agendado'
        ).count()
        
        # Serviços
        context['servicos_em_progresso'] = Servico.objects.filter(
            status='em_execucao'
        ).count()
        context['servicos_concluidos_mes'] = Servico.objects.filter(
            status='concluido',
            data_fim__month=hoje.month,
            data_fim__year=hoje.year
        ).count()
        
        # Estoque
        context['pecas_estoque_baixo'] = Peca.objects.filter(
            quantidade_atual__lte=F('quantidade_minima'),
            ativo=True
        ).count()
        
        # Financeiro
        context['contas_receber_vencidas'] = ContaReceber.objects.filter(
            status='vencida'
        ).count()
        context['contas_pagar_vencidas'] = ContaPagar.objects.filter(
            status='vencida'
        ).count()
        
        # Agendamentos recentes
        context['agendamentos_recentes'] = Agendamento.objects.filter(
            ativo=True
        ).select_related('veiculo', 'cliente', 'mecanico__user')[:10]
        
        return context


@require_http_methods(["GET", "POST"])
def create_superuser_view(request):
    """
    View temporária para criar superusuário via web.
    Só funciona se não houver superusuário e se a chave secreta estiver correta.
    IMPORTANTE: Remova esta view após criar o superusuário!
    """
    # Verifica se já existe superusuário
    if User.objects.filter(is_superuser=True).exists():
        messages.error(request, 'Superusuário já existe. Use a opção de resetar senha.')
        return redirect('core:reset_superuser')
    
    # Verifica chave secreta (opcional, mas recomendado)
    secret_key = os.environ.get('CREATE_SUPERUSER_KEY', 'temporary-key-change-me')
    provided_key = request.GET.get('key') or request.POST.get('key')
    
    if request.method == 'POST':
        if provided_key != secret_key:
            messages.error(request, 'Chave de acesso inválida.')
            return render(request, 'core/create_superuser.html', {'error': 'Chave inválida'})
        
        username = request.POST.get('username', 'admin')
        email = request.POST.get('email', 'admin@example.com')
        password = request.POST.get('password')
        
        if not password:
            messages.error(request, 'Senha é obrigatória.')
            return render(request, 'core/create_superuser.html', {'error': 'Senha obrigatória'})
        
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, f'Superusuário "{username}" criado com sucesso!')
            return redirect('admin:login')
        except Exception as e:
            messages.error(request, f'Erro ao criar superusuário: {e}')
            return render(request, 'core/create_superuser.html', {'error': str(e)})
    
    # GET request - mostra formulário
    if provided_key != secret_key:
        messages.warning(request, 'Acesso requer chave secreta via parâmetro ?key=')
        return render(request, 'core/create_superuser.html', {'require_key': True})
    
    return render(request, 'core/create_superuser.html')


@require_http_methods(["GET", "POST"])
def reset_superuser_view(request):
    """
    View temporária para resetar senha do superusuário via web.
    IMPORTANTE: Remova esta view após usar por questões de segurança!
    """
    # Verifica chave secreta
    secret_key = os.environ.get('CREATE_SUPERUSER_KEY', 'temporary-key-change-me')
    provided_key = request.GET.get('key') or request.POST.get('key')
    
    if request.method == 'POST':
        if provided_key != secret_key:
            messages.error(request, 'Chave de acesso inválida.')
            return render(request, 'core/reset_superuser.html', {'error': 'Chave inválida'})
        
        username = request.POST.get('username', 'admin')
        password = request.POST.get('password')
        
        if not password:
            messages.error(request, 'Senha é obrigatória.')
            return render(request, 'core/reset_superuser.html', {'error': 'Senha obrigatória'})
        
        try:
            user = User.objects.get(username=username, is_superuser=True)
            user.set_password(password)
            user.save()
            messages.success(request, f'Senha do superusuário "{username}" resetada com sucesso!')
            return redirect('admin:login')
        except User.DoesNotExist:
            messages.error(request, f'Superusuário "{username}" não encontrado.')
            return render(request, 'core/reset_superuser.html', {'error': f'Usuário "{username}" não encontrado'})
        except Exception as e:
            messages.error(request, f'Erro ao resetar senha: {e}')
            return render(request, 'core/reset_superuser.html', {'error': str(e)})
    
    # GET request - mostra formulário
    if provided_key != secret_key:
        messages.warning(request, 'Acesso requer chave secreta via parâmetro ?key=')
        return render(request, 'core/reset_superuser.html', {'require_key': True})
    
    return render(request, 'core/reset_superuser.html')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def buscar_cep_api(request):
    """
    Endpoint para buscar endereço por CEP via AJAX.
    
    Retorna JSON com:
    {
        'success': bool,
        'data': {
            'rua': str,
            'bairro': str,
            'cidade': str,
            'estado': str,
            'cep': str
        },
        'error': str (se success=False)
    }
    """
    cep = request.GET.get('cep') or request.POST.get('cep', '').strip()
    
    if not cep:
        return JsonResponse({
            'success': False,
            'error': 'CEP é obrigatório'
        }, status=400)
    
    # Busca endereço usando o serviço
    endereco = CEPService.buscar_endereco(cep)
    
    if endereco:
        return JsonResponse({
            'success': True,
            'data': endereco
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'CEP não encontrado ou inválido'
        }, status=404)


