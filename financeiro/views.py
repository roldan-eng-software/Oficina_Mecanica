"""
Views do app financeiro.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import ContaReceber, ContaPagar, PagamentoServico
from .forms import ContaReceberForm, ContaPagarForm, PagamentoServicoForm


class ContaReceberListView(LoginRequiredMixin, ListView):
    """Lista todas as contas a receber."""
    model = ContaReceber
    template_name = 'financeiro/conta_list.html'
    context_object_name = 'contas'
    paginate_by = 20

    def get_queryset(self):
        queryset = ContaReceber.objects.select_related('cliente', 'servico').all()
        status = self.request.GET.get('status', '')
        vencidas = self.request.GET.get('vencidas', '')
        
        if status:
            queryset = queryset.filter(status=status)
        
        if vencidas == 'true':
            queryset = queryset.filter(status='aberta', data_vencimento__lt=timezone.now().date())
        
        return queryset.order_by('-data_vencimento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = 'receber'
        context['status'] = self.request.GET.get('status', '')
        context['vencidas'] = self.request.GET.get('vencidas', '')
        return context


class ContaPagarListView(LoginRequiredMixin, ListView):
    """Lista todas as contas a pagar."""
    model = ContaPagar
    template_name = 'financeiro/conta_list.html'
    context_object_name = 'contas'
    paginate_by = 20

    def get_queryset(self):
        queryset = ContaPagar.objects.select_related('fornecedor').all()
        status = self.request.GET.get('status', '')
        vencidas = self.request.GET.get('vencidas', '')
        
        if status:
            queryset = queryset.filter(status=status)
        
        if vencidas == 'true':
            queryset = queryset.filter(status='aberta', data_vencimento__lt=timezone.now().date())
        
        return queryset.order_by('-data_vencimento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = 'pagar'
        context['status'] = self.request.GET.get('status', '')
        context['vencidas'] = self.request.GET.get('vencidas', '')
        return context


class ContaReceberCreateView(LoginRequiredMixin, CreateView):
    """Criar nova conta a receber."""
    model = ContaReceber
    form_class = ContaReceberForm
    template_name = 'financeiro/conta_form.html'
    success_url = reverse_lazy('financeiro:conta_receber_list')

    def form_valid(self, form):
        messages.success(self.request, 'Conta a receber criada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = 'receber'
        return context


class ContaPagarCreateView(LoginRequiredMixin, CreateView):
    """Criar nova conta a pagar."""
    model = ContaPagar
    form_class = ContaPagarForm
    template_name = 'financeiro/conta_form.html'
    success_url = reverse_lazy('financeiro:conta_pagar_list')

    def form_valid(self, form):
        messages.success(self.request, 'Conta a pagar criada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = 'pagar'
        return context


class DashboardFinanceiroView(LoginRequiredMixin, TemplateView):
    """Dashboard financeiro com estatísticas."""
    template_name = 'financeiro/dashboard_financeiro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        hoje = timezone.now().date()
        mes_atual = hoje.month
        ano_atual = hoje.year
        
        # Contas a Receber
        context['total_receber'] = ContaReceber.objects.filter(status='aberta').aggregate(
            total=Sum('valor')
        )['total'] or 0
        
        context['total_recebido_mes'] = ContaReceber.objects.filter(
            status='paga',
            data_pagamento__month=mes_atual,
            data_pagamento__year=ano_atual
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        context['contas_vencidas_receber'] = ContaReceber.objects.filter(
            status='aberta',
            data_vencimento__lt=hoje
        ).count()
        
        # Contas a Pagar
        context['total_pagar'] = ContaPagar.objects.filter(status='aberta').aggregate(
            total=Sum('valor')
        )['total'] or 0
        
        context['total_pago_mes'] = ContaPagar.objects.filter(
            status='paga',
            data_pagamento__month=mes_atual,
            data_pagamento__year=ano_atual
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        context['contas_vencidas_pagar'] = ContaPagar.objects.filter(
            status='aberta',
            data_vencimento__lt=hoje
        ).count()
        
        # Saldo
        context['saldo_mes'] = context['total_recebido_mes'] - context['total_pago_mes']
        
        return context


class RelatorioFinanceiroView(LoginRequiredMixin, TemplateView):
    """Relatório financeiro."""
    template_name = 'financeiro/relatorio_financeiro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Implementação futura para relatórios detalhados
        return context

