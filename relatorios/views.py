from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

from clientes.models import Cliente
from veiculos.models import Veiculo
from agendamentos.models import Agendamento
from servicos.models import Servico
from estoque.models import Peca
from financeiro.models import ContaReceber, ContaPagar, PagamentoServico


def generate_pdf_response(template_name, context, filename):
    """
    Gera resposta PDF a partir de um template HTML.
    Requer WeasyPrint instalado.
    """
    if not WEASYPRINT_AVAILABLE:
        return HttpResponse(
            "WeasyPrint não está instalado. Execute: pip install weasyprint",
            status=500
        )
    
    html_string = render_to_string(template_name, context)
    html = HTML(string=html_string, base_url='/')
    
    # CSS básico para impressão
    css = CSS(string="""
        @page { margin: 1cm; }
        body { font-family: Arial, Helvetica, sans-serif; }
    """)
    
    pdf = html.write_pdf(stylesheets=[css])
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def clientes_print(request):
    clientes = Cliente.objects.all().order_by('nome')
    return render(request, 'relatorios/clientes_list_print.html', {'clientes': clientes})


@login_required
def clientes_pdf(request):
    clientes = Cliente.objects.all().order_by('nome')
    return generate_pdf_response(
        'relatorios/clientes_list_print.html',
        {'clientes': clientes},
        'clientes.pdf'
    )


@login_required
def veiculos_print(request):
    veiculos = Veiculo.objects.select_related('cliente').all().order_by('placa')
    return render(request, 'relatorios/veiculos_list_print.html', {'veiculos': veiculos})


@login_required
def veiculos_pdf(request):
    veiculos = Veiculo.objects.select_related('cliente').all().order_by('placa')
    return generate_pdf_response(
        'relatorios/veiculos_list_print.html',
        {'veiculos': veiculos},
        'veiculos.pdf'
    )


@login_required
def agendamentos_print(request):
    agendamentos = Agendamento.objects.select_related('veiculo', 'cliente').all().order_by('-data_hora')
    return render(request, 'relatorios/agendamentos_list_print.html', {'agendamentos': agendamentos})


@login_required
def agendamentos_pdf(request):
    agendamentos = Agendamento.objects.select_related('veiculo', 'cliente').all().order_by('-data_hora')
    return generate_pdf_response(
        'relatorios/agendamentos_list_print.html',
        {'agendamentos': agendamentos},
        'agendamentos.pdf'
    )


@login_required
def servicos_print(request):
    servicos = Servico.objects.select_related('agendamento__veiculo').all().order_by('-created_at')
    return render(request, 'relatorios/servicos_list_print.html', {'servicos': servicos})


@login_required
def servicos_pdf(request):
    servicos = Servico.objects.select_related('agendamento__veiculo').all().order_by('-created_at')
    return generate_pdf_response(
        'relatorios/servicos_list_print.html',
        {'servicos': servicos},
        'servicos.pdf'
    )


@login_required
def estoque_print(request):
    pecas = Peca.objects.select_related('fornecedor').all().order_by('descricao')
    return render(request, 'relatorios/estoque_list_print.html', {'pecas': pecas})


@login_required
def estoque_pdf(request):
    pecas = Peca.objects.select_related('fornecedor').all().order_by('descricao')
    return generate_pdf_response(
        'relatorios/estoque_list_print.html',
        {'pecas': pecas},
        'estoque.pdf'
    )


@login_required
def financeiro_print(request):
    contas_receber = ContaReceber.objects.select_related('cliente').all().order_by('-data_vencimento')
    contas_pagar = ContaPagar.objects.select_related('fornecedor').all().order_by('-data_vencimento')
    pagamentos = PagamentoServico.objects.select_related('servico').all().order_by('-data')
    return render(request, 'relatorios/financeiro_list_print.html', {
        'contas_receber': contas_receber,
        'contas_pagar': contas_pagar,
        'pagamentos': pagamentos,
    })


@login_required
def financeiro_pdf(request):
    contas_receber = ContaReceber.objects.select_related('cliente').all().order_by('-data_vencimento')
    contas_pagar = ContaPagar.objects.select_related('fornecedor').all().order_by('-data_vencimento')
    pagamentos = PagamentoServico.objects.select_related('servico').all().order_by('-data')
    return generate_pdf_response(
        'relatorios/financeiro_list_print.html',
        {
            'contas_receber': contas_receber,
            'contas_pagar': contas_pagar,
            'pagamentos': pagamentos,
        },
        'financeiro.pdf'
    )

