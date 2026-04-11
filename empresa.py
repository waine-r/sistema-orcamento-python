from banco import carregar_dados, salvar_dados


# Função para cadastrar empresa
def cadastrar_empresa():
    dados = carregar_dados()

    # Verifica se já existe empresa cadastrada
    if "empresa" in dados:
        print("Empresa já cadastrada!")
        return

    print("=== Cadastro da Empresa ===")

    nome = input("Nome da empresa: ")
    cnpj = input("CNPJ: ")
    endereco = input("Endereço: ")
    telefone = input("Telefone: ")
    logo = input("Caminho da logo (opcional): ")

    # Criando estrutura da empresa
    dados["empresa"] = {
        "nome": nome,
        "cnpj": cnpj,
        "endereco": endereco,
        "telefone": telefone,
        "logo": logo
    }

    salvar_dados(dados)

    print("Empresa cadastrada com sucesso!")