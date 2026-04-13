# Função para ler um número inteiro com segurança
def ler_int(mensagem):
    while True:  # loop infinito até o usuário acertar
        try:
            valor = int(input(mensagem))  # tenta converter para inteiro
            return valor  # retorna o valor válido
        except ValueError:  # se der erro (letra, vazio, etc)
            print("❌ Digite um número válido!")


# Função para ler número decimal (float)
def ler_float(mensagem):
    while True:  # continua até acertar
        try:
            valor = float(input(mensagem))  # tenta converter para float
            return valor  # retorna valor válido
        except ValueError:
            print("❌ Digite um número válido!")


# Função para escolher opção dentro de uma lista
def escolher_opcao(lista, mensagem):
    while True:
        escolha = ler_int(mensagem) - 1  # ajusta índice (usuário começa em 1)

        # verifica se está dentro do intervalo
        if 0 <= escolha < len(lista):
            return escolha  # retorna índice válido
        else:
            print("❌ Opção inválida! Tente novamente.")