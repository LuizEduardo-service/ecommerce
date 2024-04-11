from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from . import models
from perfil.models import Perfil

from django.db.models import Q


# Create your views here.

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 3

class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs
        
        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains = termo) |
            Q(descricao_curta__icontains = termo) |
            Q(descricao_longa__icontains = termo) 
        )

        self.request.session.save()
        return qs
class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarCarrinho(View):
    def get(self,*args, **kwargs):

        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()

        http_referencia = self.request.META.get('HTTP_REFERER',reverse('produto:lista')) # VOLTA PARA A URL DE ONDE FOI CHAMADA
        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            messages.error(
                self.request,
                "produto não existe"
            )
            redirect(http_referencia)
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.pk
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ""
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug 
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ""

        # verifica se possui estoque
        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque Insuficiente'
            )
            return redirect(http_referencia)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
        
        carrinho = self.request.session.get('carrinho')

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    'Estoque Insuficiente'
                )
                quantidade_carrinho = variacao_estoque
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                    'produto_id': produto_id, 
                    'produto_nome': produto_nome, 
                    'variacao_nome': variacao_nome, 
                    'variacao_id': variacao_id, 
                    'preco_unitario': preco_unitario, 
                    'preco_unitario_promocional': preco_unitario_promocional, 
                    'preco_quantitativo': preco_unitario,
                    'preco_quantitativo_promocional': preco_unitario_promocional, 
                    'quantidade': 1, 
                    'slug': slug, 
                    'imagem': imagem
            }
        self.request.session.save()
        messages.success(
            self.request,
            'Produto Inserido com Sucesso ao Carrinho!'
        )
        print(carrinho)
        return redirect(http_referencia)

class RemoverCarrinho(View):
    def get(self,*args, **kwargs):
        http_referencia = self.request.META.get('HTTP_REFERER',reverse('produto:lista')) # VOLTA PARA A URL DE ONDE FOI CHAMADA
        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            return redirect(http_referencia)

        if not self.request.session.get('carrinho'):
            return redirect(http_referencia)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referencia)
        
        carrinho = self.request.session['carrinho'][variacao_id]
        messages.success(
            self.request,
            f'Produto {carrinho['produto_nome']} removido:'
        )
        
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referencia)

class Carrinho(View):
    def get(self,*args, **kwargs):
        context = {
            'carrinho': self.request.session.get('carrinho')
        }
        return render(self.request, 'produto/carrinho.html', context=context)

class ResumoCompra(View):
    def get(self,*args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        

        perfil = Perfil.objects.filter(user=self.request.user).exists()

        if not perfil:
            messages.error(self.request, "Usuario sem Perfil de Compra")
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(self.request, "Você não tem itens no carrinho.")
            return redirect('produto:lista')

        self.contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho']
        }
        return render(self.request, 'produto/resumo_compra.html', self.contexto)


