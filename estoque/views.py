"""
Views do app estoque.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, F

from .models import Peca, MovimentacaoPeca, Fornecedor
from .forms import PecaForm, MovimentacaoPecaForm, FornecedorForm


class PecaListView(LoginRequiredMixin, ListView):
    """Lista todas as peças."""
    model = Peca
    template_name = 'estoque/peca_list.html'
    context_object_name = 'pecas'
    paginate_by = 20

    def get_queryset(self):
        queryset = Peca.objects.select_related('fornecedor').all()
        search = self.request.GET.get('search', '')
        categoria = self.request.GET.get('categoria', '')
        estoque_baixo = self.request.GET.get('estoque_baixo', '')
        
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) |
                Q(descricao__icontains=search) |
                Q(fabricante__icontains=search)
            )
        
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        if estoque_baixo == 'true':
            queryset = queryset.filter(quantidade_atual__lte=F('quantidade_minima'))
        
        return queryset.order_by('descricao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['categoria'] = self.request.GET.get('categoria', '')
        context['estoque_baixo'] = self.request.GET.get('estoque_baixo', '')
        return context


class PecaDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de uma peça."""
    model = Peca
    template_name = 'estoque/peca_detail.html'
    context_object_name = 'peca'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movimentacoes'] = self.object.movimentacoes.filter(ativo=True)[:10]
        return context


class PecaCreateView(LoginRequiredMixin, CreateView):
    """Criar nova peça."""
    model = Peca
    form_class = PecaForm
    template_name = 'estoque/peca_form.html'
    success_url = reverse_lazy('estoque:peca_list')

    def form_valid(self, form):
        messages.success(self.request, 'Peça criada com sucesso!')
        return super().form_valid(form)


class PecaUpdateView(LoginRequiredMixin, UpdateView):
    """Atualizar peça existente."""
    model = Peca
    form_class = PecaForm
    template_name = 'estoque/peca_form.html'
    success_url = reverse_lazy('estoque:peca_list')

    def form_valid(self, form):
        messages.success(self.request, 'Peça atualizada com sucesso!')
        return super().form_valid(form)


class MovimentacaoPecaListView(LoginRequiredMixin, ListView):
    """Lista todas as movimentações."""
    model = MovimentacaoPeca
    template_name = 'estoque/movimentacao_list.html'
    context_object_name = 'movimentacoes'
    paginate_by = 20

    def get_queryset(self):
        queryset = MovimentacaoPeca.objects.select_related('peca', 'usuario_responsavel__user').all()
        peca_id = self.request.GET.get('peca', '')
        tipo = self.request.GET.get('tipo', '')
        
        if peca_id:
            queryset = queryset.filter(peca_id=peca_id)
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        return queryset.order_by('-data_movimentacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['peca_id'] = self.request.GET.get('peca', '')
        context['tipo'] = self.request.GET.get('tipo', '')
        return context


class MovimentacaoPecaCreateView(LoginRequiredMixin, CreateView):
    """Criar nova movimentação."""
    model = MovimentacaoPeca
    form_class = MovimentacaoPecaForm
    template_name = 'estoque/movimentacao_form.html'
    success_url = reverse_lazy('estoque:movimentacao_list')

    def form_valid(self, form):
        # Define o usuário responsável como o usuário atual se não foi especificado
        if not form.cleaned_data.get('usuario_responsavel'):
            from core.models import Usuario
            try:
                usuario = Usuario.objects.get(user=self.request.user)
                form.instance.usuario_responsavel = usuario
            except Usuario.DoesNotExist:
                pass
        
        messages.success(self.request, 'Movimentação registrada com sucesso!')
        return super().form_valid(form)

