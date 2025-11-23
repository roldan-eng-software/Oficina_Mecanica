"""
Views do app veiculos.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Veiculo
from .forms import VeiculoForm


class VeiculoListView(LoginRequiredMixin, ListView):
    """Lista todos os veículos."""
    model = Veiculo
    template_name = 'veiculos/veiculo_list.html'
    context_object_name = 'veiculos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Veiculo.objects.select_related('cliente').all()
        search = self.request.GET.get('search', '')
        cliente_id = self.request.GET.get('cliente', '')
        
        if search:
            queryset = queryset.filter(
                Q(placa__icontains=search) |
                Q(marca__icontains=search) |
                Q(modelo__icontains=search) |
                Q(chassis__icontains=search) |
                Q(cliente__nome__icontains=search)
            )
        
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        return queryset.order_by('placa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['cliente_id'] = self.request.GET.get('cliente', '')
        from clientes.models import Cliente
        context['clientes'] = Cliente.objects.filter(ativo=True).order_by('nome')
        return context


class VeiculoDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de um veículo."""
    model = Veiculo
    template_name = 'veiculos/veiculo_detail.html'
    context_object_name = 'veiculo'


class VeiculoCreateView(LoginRequiredMixin, CreateView):
    """Criar novo veículo."""
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculos/veiculo_form.html'
    success_url = reverse_lazy('veiculos:veiculo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Veículo criado com sucesso!')
        return super().form_valid(form)


class VeiculoUpdateView(LoginRequiredMixin, UpdateView):
    """Atualizar veículo existente."""
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculos/veiculo_form.html'
    success_url = reverse_lazy('veiculos:veiculo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Veículo atualizado com sucesso!')
        return super().form_valid(form)


class VeiculoDeleteView(LoginRequiredMixin, DeleteView):
    """Excluir veículo."""
    model = Veiculo
    template_name = 'veiculos/veiculo_confirm_delete.html'
    success_url = reverse_lazy('veiculos:veiculo_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Veículo excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

