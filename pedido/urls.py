from django.urls import path
from . import views

urlpatterns = [
    path('pagar/', views.Pagar.as_view(), name='pagar'),
    path('fecharpedido/', views.FecharPedido.as_view(), name='fecharpedido'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),

] 