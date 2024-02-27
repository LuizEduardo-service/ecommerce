from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from . import models


# Create your views here.

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    
class DetalheProduto(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Detalhe Produto')

class AdicionarCarrinho(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Adicionar Carrinho')

class RemoverCarrinho(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Remover Carrinho')

class Carrinho(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Carrinho')

class Finalizar(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Finalizar')
