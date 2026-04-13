from banco import carregar_dados, salvar_dados


# Função para cadastrar empresa
def cadastrar_empresa():
    dados = carregar_dados()

    from tkinter import messagebox  # IMPORTANTE (coloque no topo do arquivo)

    if "empresa" in dados:
        messagebox.showwarning("Aviso", "Empresa já cadastrada!")
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