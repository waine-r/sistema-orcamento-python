import tkinter as tk  # biblioteca para criar interface gráfica

# importa funções do seu sistema
from empresa import cadastrar_empresa
from cliente import cadastrar_cliente, listar_clientes
from orcamento import criar_orcamento, listar_orcamentos, excluir_orcamento, gerar_pdf_orcamento


# função principal da interface
def iniciar_interface():

    janela = tk.Tk()  # cria a janela principal
    janela.title("Sistema de Orçamentos")  # título da janela
    janela.geometry("400x500")  # tamanho da janela

    # título no topo
    titulo = tk.Label(janela, text="Sistema de Orçamentos", font=("Arial", 16))
    titulo.pack(pady=20)  # adiciona espaço

    # botão cadastrar empresa
    btn_empresa = tk.Button(janela, text="Cadastrar Empresa", width=30, command=cadastrar_empresa)
    btn_empresa.pack(pady=5)

    # botão cadastrar cliente
    btn_cliente = tk.Button(janela, text="Cadastrar Cliente", width=30, command=tela_cadastrar_cliente)
    btn_cliente.pack(pady=5)

    # botão listar clientes
    btn_listar_clientes = tk.Button(janela, text="Listar Clientes", width=30, command=tela_listar_clientes)
    btn_listar_clientes.pack(pady=5)

    # botão criar orçamento
    btn_orcamento = tk.Button(janela, text="Criar Orçamento", width=30, command=criar_orcamento)
    btn_orcamento.pack(pady=5)

    # botão listar orçamentos
    btn_listar_orc = tk.Button(janela, text="Listar Orçamentos", width=30, command=listar_orcamentos)
    btn_listar_orc.pack(pady=5)

    # botão excluir orçamento
    btn_excluir = tk.Button(janela, text="Excluir Orçamento", width=30, command=excluir_orcamento)
    btn_excluir.pack(pady=5)

    # botão gerar PDF
    btn_pdf = tk.Button(janela, text="Gerar PDF", width=30, command=gerar_pdf_orcamento)
    btn_pdf.pack(pady=5)

    # botão sair
    btn_sair = tk.Button(janela, text="Sair", width=30, command=janela.destroy)
    btn_sair.pack(pady=20)

    janela.mainloop()  # mantém a janela aberta

# tela para cadastrar cliente (100% gráfica)
def tela_cadastrar_cliente():

    # cria nova janela
    janela = tk.Toplevel()
    janela.title("Cadastrar Cliente")
    janela.geometry("300x300")

    # campo nome
    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    # campo telefone
    tk.Label(janela, text="Telefone").pack()
    entry_telefone = tk.Entry(janela)
    entry_telefone.pack()

    # campo email
    tk.Label(janela, text="Email").pack()
    entry_email = tk.Entry(janela)
    entry_email.pack()

    # campo endereço
    tk.Label(janela, text="Endereço").pack()
    entry_endereco = tk.Entry(janela)
    entry_endereco.pack()

    # função que salva os dados
    def salvar():
        from banco import carregar_dados, salvar_dados  # importa aqui dentro

        dados = carregar_dados()  # carrega dados existentes

        # se não existir lista de clientes, cria
        if "clientes" not in dados:
            dados["clientes"] = []

        # cria cliente com dados da tela
        cliente = {
            "nome": entry_nome.get(),  # pega texto digitado
            "telefone": entry_telefone.get(),
            "email": entry_email.get(),
            "endereco": entry_endereco.get()
        }

        dados["clientes"].append(cliente)  # adiciona cliente

        salvar_dados(dados)  # salva no JSON

        print("Cliente salvo com sucesso!")  # feedback no terminal

        janela.destroy()  # fecha a janela

    # botão salvar
    tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

# tela para listar clientes na interface
def tela_listar_clientes():

    from banco import carregar_dados  # importa função para carregar dados

    dados = carregar_dados()  # carrega dados do JSON

    # cria nova janela
    janela = tk.Toplevel()
    janela.title("Lista de Clientes")
    janela.geometry("400x400")

    tk.Label(janela, text="Clientes cadastrados", font=("Arial", 14)).pack(pady=10)

    # verifica se há clientes
    if "clientes" not in dados or len(dados["clientes"]) == 0:
        tk.Label(janela, text="Nenhum cliente cadastrado").pack()
        return

    # lista os clientes
    for cliente in dados["clientes"]:
        texto = f"{cliente['nome']} - {cliente['telefone']}"

        tk.Label(janela, text=texto, anchor="w").pack(fill="x", padx=10, pady=2)