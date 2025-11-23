"""
Views do app agendamentos.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Agendamento
from .forms import AgendamentoForm


class AgendamentoListView(LoginRequiredMixin, ListView):
    """Lista todos os agendamentos."""
    model = Agendamento
    template_name = 'agendamentos/agendamento_list.html'
    context_object_name = 'agendamentos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Agendamento.objects.select_related('veiculo', 'cliente', 'mecanico__user').all()
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        data_inicio = self.request.GET.get('data_inicio', '')
        data_fim = self.request.GET.get('data_fim', '')
        
        if search:
            queryset = queryset.filter(
                Q(veiculo__placa__icontains=search) |
                Q(cliente__nome__icontains=search) |
                Q(descricao_problema__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        if data_inicio:
            try:
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                queryset = queryset.filter(data_hora__date__gte=data_inicio)
            except ValueError:
                pass
        
        if data_fim:
            try:
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
                queryset = queryset.filter(data_hora__date__lte=data_fim)
            except ValueError:
                pass
        
        return queryset.order_by('-data_hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['data_inicio'] = self.request.GET.get('data_inicio', '')
        context['data_fim'] = self.request.GET.get('data_fim', '')
        return context


class AgendamentoDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de um agendamento."""
    model = Agendamento
    template_name = 'agendamentos/agendamento_detail.html'
    context_object_name = 'agendamento'


class AgendamentoCreateView(LoginRequiredMixin, CreateView):
    """Criar novo agendamento."""
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/agendamento_form.html'
    success_url = reverse_lazy('agendamentos:agendamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Agendamento criado com sucesso!')
        return super().form_valid(form)


class AgendamentoUpdateView(LoginRequiredMixin, UpdateView):
    """Atualizar agendamento existente."""
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/agendamento_form.html'
    success_url = reverse_lazy('agendamentos:agendamento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Agendamento atualizado com sucesso!')
        return super().form_valid(form)


class AgendamentoDeleteView(LoginRequiredMixin, DeleteView):
    """Excluir agendamento."""
    model = Agendamento
    template_name = 'agendamentos/agendamento_confirm_delete.html'
    success_url = reverse_lazy('agendamentos:agendamento_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Agendamento excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class CalendarioView(LoginRequiredMixin, ListView):
    """Visualização em calendário dos agendamentos."""
    model = Agendamento
    template_name = 'agendamentos/calendario.html'
    context_object_name = 'agendamentos'

    def get_queryset(self):
        mes = self.request.GET.get('mes', timezone.now().month)
        ano = self.request.GET.get('ano', timezone.now().year)
        return Agendamento.objects.filter(
            data_hora__month=mes,
            data_hora__year=ano,
            ativo=True
        ).select_related('veiculo', 'cliente', 'mecanico__user').order_by('data_hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mes'] = int(self.request.GET.get('mes', timezone.now().month))
        context['ano'] = int(self.request.GET.get('ano', timezone.now().year))
        return context

