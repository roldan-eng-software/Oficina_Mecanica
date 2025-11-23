"""
Views do app clientes.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Cliente
from .forms import ClienteForm


class ClienteListView(LoginRequiredMixin, ListView):
    """Lista todos os clientes."""
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Cliente.objects.all()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(cpf_cnpj__icontains=search) |
                Q(email__icontains=search) |
                Q(telefone__icontains=search)
            )
        return queryset.order_by('nome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class ClienteDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de um cliente."""
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'


class ClienteCreateView(LoginRequiredMixin, CreateView):
    """Criar novo cliente."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente criado com sucesso!')
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    """Atualizar cliente existente."""
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    """Excluir cliente."""
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cliente excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

