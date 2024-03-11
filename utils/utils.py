
def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.',',')

def cart_total_qtd(carrinho):
    return sum([i['quantidade'] for i in carrinho.values()])

def cart_totals(carrinho):
    return formata_preco(sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item 
            in carrinho.values()
        ]
    ))
