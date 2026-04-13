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
    btn_cliente = tk.Button(janela, text="Cadastrar Cliente", width=30, command=cadastrar_cliente)
    btn_cliente.pack(pady=5)

    # botão listar clientes
    btn_listar_clientes = tk.Button(janela, text="Listar Clientes", width=30, command=listar_clientes)
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