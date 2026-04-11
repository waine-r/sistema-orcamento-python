# Importa funções do arquivo banco.py
from banco import carregar_dados, salvar_dados


# Função para cadastrar um novo cliente
def cadastrar_cliente():
    # Carrega os dados existentes do arquivo JSON
    dados = carregar_dados()

    # Verifica se já existe a chave "clientes" no dicionário
    # Se não existir, cria uma lista vazia
    if "clientes" not in dados:
        dados["clientes"] = []

    print("\n=== Cadastro de Cliente ===")

    # Coleta informações do usuário
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    endereco = input("Endereço: ")

    # Cria um dicionário representando o cliente
    cliente = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "endereco": endereco
    }

    # Adiciona o cliente na lista de clientes
    dados["clientes"].append(cliente)

    # Salva os dados atualizados no arquivo JSON
    salvar_dados(dados)

    print("Cliente cadastrado com sucesso!")


# Função para listar todos os clientes cadastrados
def listar_clientes():
    # Carrega os dados do arquivo
    dados = carregar_dados()

    # Verifica se existem clientes cadastrados
    if "clientes" not in dados or len(dados["clientes"]) == 0:
        print("Nenhum cliente cadastrado.")
        return  # Encerra a função

    print("\n=== Lista de Clientes ===")

    # Percorre a lista de clientes com índice (enumerate)
    for i, cliente in enumerate(dados["clientes"]):
        # i começa em 0, então usamos i+1 para ficar mais amigável
        print(f"{i + 1} - {cliente['nome']} - {cliente['telefone']}")