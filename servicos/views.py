"""
Views do app servicos.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Sum

from .models import Servico, Orcamento
from .forms import ServicoForm, OrcamentoForm


class ServicoListView(LoginRequiredMixin, ListView):
    """Lista todos os serviços."""
    model = Servico
    template_name = 'servicos/servico_list.html'
    context_object_name = 'servicos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Servico.objects.select_related('agendamento__veiculo', 'agendamento__cliente').all()
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        
        if search:
            queryset = queryset.filter(
                Q(agendamento__veiculo__placa__icontains=search) |
                Q(agendamento__cliente__nome__icontains=search) |
                Q(descricao_trabalho__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        return context


class ServicoDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de um serviço."""
    model = Servico
    template_name = 'servicos/servico_detail.html'
    context_object_name = 'servico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orcamentos'] = self.object.orcamentos.filter(ativo=True)
        return context


class ServicoCreateView(LoginRequiredMixin, CreateView):
    """Criar novo serviço."""
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/servico_form.html'
    success_url = reverse_lazy('servicos:servico_list')

    def form_valid(self, form):
        messages.success(self.request, 'Serviço criado com sucesso!')
        return super().form_valid(form)


class ServicoUpdateView(LoginRequiredMixin, UpdateView):
    """Atualizar serviço existente."""
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/servico_form.html'
    success_url = reverse_lazy('servicos:servico_list')

    def form_valid(self, form):
        messages.success(self.request, 'Serviço atualizado com sucesso!')
        return super().form_valid(form)


class OrcamentoListView(LoginRequiredMixin, ListView):
    """Lista todos os orçamentos."""
    model = Orcamento
    template_name = 'servicos/orcamento_list.html'
    context_object_name = 'orcamentos'
    paginate_by = 20

    def get_queryset(self):
        servico_id = self.request.GET.get('servico', '')
        queryset = Orcamento.objects.select_related('servico').all()
        
        if servico_id:
            queryset = queryset.filter(servico_id=servico_id)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servico_id'] = self.request.GET.get('servico', '')
        return context


class OrcamentoDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de um orçamento."""
    model = Orcamento
    template_name = 'servicos/orcamento_detail.html'
    context_object_name = 'orcamento'

