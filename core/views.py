"""
Views do app core.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q, F
from datetime import datetime, timedelta

from clientes.models import Cliente
from veiculos.models import Veiculo
from agendamentos.models import Agendamento
from servicos.models import Servico
from estoque.models import Peca
from financeiro.models import ContaReceber, ContaPagar


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

