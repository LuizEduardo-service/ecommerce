from django.urls import path
from . import views

urlpatterns = [
    path('pagar/', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),

] 