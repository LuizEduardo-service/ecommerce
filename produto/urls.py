from django.urls import path
from . import views

app_name = 'produto'
urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe'),
    path('adicionarcarino', views.AdicionarCarrinho.as_view(), name='adicionarcarrinho'),
    path('removercarino', views.RemoverCarrinho.as_view(), name='removercarrinho'),
    path('carrinho', views.Carrinho.as_view(), name='carrinho'),
    path('finalizar', views.Finalizar.as_view(), name='finalizar'),
] 