from django.contrib import admin
from .models import *


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
    ItemPedidoInline
    ]


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
