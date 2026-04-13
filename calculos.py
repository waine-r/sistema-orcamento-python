# Função para calcular subtotal de um item
def calcular_subtotal(quantidade, valor_unitario):
    return quantidade * valor_unitario  # multiplica quantidade pelo valor


# Função para calcular total do orçamento
def calcular_total(itens):
    return sum(item["subtotal"] for item in itens)  # soma todos os subtotais