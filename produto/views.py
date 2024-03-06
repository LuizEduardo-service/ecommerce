from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from . import models


# Create your views here.

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 3
    
class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarCarrinho(View):
    def get(self,*args, **kwargs):
        http_referencia = self.request.META.get('HTTP_REFERER',reverse('produto:lista')) # VOLTA PARA A URL DE ONDE FOI CHAMADA
        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            messages.error(
                self.request,
                "produto não existe"
            )
            redirect(http_referencia)
        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
        
        carrinho = self.request.session.get('carrinho')

        if variacao_id in carrinho:
            pass
        else:
            pass
        
        return HttpResponse(f'Adicionar Carrinho: {variacao.produto}')

class RemoverCarrinho(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Remover Carrinho')

class Carrinho(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Carrinho')

class Finalizar(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Finalizar')
