from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import ListView, DeleteView, DetailView
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from produto.models import Variacao
from django.urls import reverse

from utils import utils
from .models import ItemPedido, Pedido

class DispathLoginRequiredMixin(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs

class Pagar(DispathLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'
    ordering = ['-id']
    



class SalvarPedido(View):
    template_name = 'pedido/pagar.html'
    def get(self,*args, **kwargs):

        if not self.request.user.is_authenticated:
            messages.error(self.request,'Usuario não esta logado')
            return redirect('perfil:criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(self.request,'Carrinho Vazio')
            return redirect('produto:lista')
        
        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]
        
        bd_variacao = list(
            Variacao.objects.select_related('produto').filter(id__in=carrinho_variacao_ids)
        )

        msg_erro_estoque = ""
        for variacao in bd_variacao:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']


            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo
                msg_erro_estoque = "'Quantidade atual em estoque insuficiente!'"

                if msg_erro_estoque:
                    messages.error(self.request, msg_erro_estoque)
                    self.request.session.save()
                    return redirect('produto:carrinho')
        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        val_total_carrinho = utils.cart_totals(carrinho)

        pedido = Pedido(
            user = self.request.user,
            total = val_total_carrinho,
            qtd_total = qtd_total_carrinho,
            status = 'C'
        )

        pedido.save()
        
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto = v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        del self.request.session['carrinho']
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )

class Detalhe(DispathLoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedido/detalhe.html'
    context_object_name = 'pedido'
    pk_url_kwarg = 'pk'
  

class Lista(DispathLoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedido/lista.html'
    context_object_name = 'pedidos'
    paginate_by = 10
