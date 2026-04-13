import tkinter as tk  # biblioteca para criar interface gráfica

# importa funções do seu sistema
from empresa import cadastrar_empresa
from cliente import cadastrar_cliente, listar_clientes
from orcamento import criar_orcamento, listar_orcamentos, excluir_orcamento, gerar_pdf_orcamento
from tkinter import messagebox  # caixa de mensagem profissional


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
    btn_orcamento = tk.Button(janela, text="Criar Orçamento", width=30, command=tela_criar_orcamento)
    btn_orcamento.pack(pady=5)

    # botão listar orçamentos
    btn_listar_orc = tk.Button(janela, text="Listar Orçamentos", width=30, command=tela_listar_orcamentos)
    btn_listar_orc.pack(pady=5)

    # botão excluir orçamento
    btn_excluir = tk.Button(janela, text="Excluir Orçamento", width=30, command=tela_excluir_orcamento)
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

    # campo cnf/cnpj
    tk.Label(janela, text="CPF/CNPJ (opcional)").pack()
    entry_doc = tk.Entry(janela)
    entry_doc.pack()

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
            "endereco": entry_endereco.get(),
            "documento": entry_doc.get()  # opcional
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

# tela para criar orçamento (interface)
def tela_criar_orcamento():

    from orcamento import gerar_numero_orcamento  # importa gerador correto
    from banco import carregar_dados, salvar_dados
    from calculos import calcular_subtotal, calcular_total
    from datetime import datetime

    dados = carregar_dados()

    # verifica clientes
    if "clientes" not in dados or len(dados["clientes"]) == 0:
        print("Cadastre um cliente primeiro!")
        return

    # cria janela
    janela = tk.Toplevel()
    janela.title("Novo Orçamento")
    janela.geometry("500x500")

    # =========================
    # CLIENTE
    # =========================

    tk.Label(janela, text="Selecione o cliente").pack()

    nomes_clientes = [c["nome"] for c in dados["clientes"]]

    cliente_var = tk.StringVar()
    cliente_var.set(nomes_clientes[0])

    dropdown = tk.OptionMenu(janela, cliente_var, *nomes_clientes)
    dropdown.pack()

    # =========================
    # ITENS
    # =========================

    itens = []

    total_var = tk.StringVar()  # variável que guarda o total na tela
    total_var.set("Total: R$ 0.00")  # valor inicial

    tk.Label(janela, text="Descrição").pack()
    entry_desc = tk.Entry(janela)
    entry_desc.pack()

    tk.Label(janela, text="Quantidade").pack()
    entry_qtd = tk.Entry(janela)
    entry_qtd.pack()

    tk.Label(janela, text="Unidade").pack()  # label unidade
    entry_unidade = tk.Entry(janela)  # campo unidade
    entry_unidade.pack()

    tk.Label(janela, text="Valor Unitário").pack()
    entry_valor = tk.Entry(janela)
    entry_valor.pack()

    lista_itens = tk.Listbox(janela, width=60)
    lista_itens.pack(pady=10)

    label_total = tk.Label(janela, textvariable=total_var, font=("Arial", 12, "bold"))
    label_total.pack()

    # =========================
    # FUNÇÃO ADICIONAR ITEM
    # =========================

    def adicionar_item():
        try:
            descricao = entry_desc.get()
            quantidade = float(entry_qtd.get())
            unidade = entry_unidade.get()  # pega unidade
            valor = float(entry_valor.get())

            subtotal = calcular_subtotal(quantidade, valor)

            item = {
                "descricao": descricao,
                "unidade": unidade,  # adiciona unidade
                "quantidade": quantidade,
                "valor_unitario": valor,
                "subtotal": subtotal
            }

            itens.append(item)

            total = calcular_total(itens)  # recalcula total
            total_var.set(f"Total: R$ {total:.2f}")  # atualiza na tela

            lista_itens.insert(
            tk.END,
            f"{descricao} | {quantidade} {unidade} | "
            f"R$ {valor:.2f} | Total: R$ {subtotal:.2f}"
        )

            # limpa campos
            entry_desc.delete(0, tk.END)
            entry_qtd.delete(0, tk.END)
            entry_valor.delete(0, tk.END)
            entry_unidade.delete(0, tk.END)  # limpa unidade

        except:
            print("Erro ao adicionar item")

    tk.Button(janela, text="Adicionar Item", command=adicionar_item).pack()

    def remover_item():
        try:
            selecionado = lista_itens.curselection()[0]  # pega índice selecionado

            lista_itens.delete(selecionado)  # remove da lista visual
            itens.pop(selecionado)  # remove da lista real

            total = calcular_total(itens)  # recalcula total
            total_var.set(f"Total: R$ {total:.2f}")  # atualiza

        except:
         print("Selecione um item para remover")

    tk.Button(janela, text="Remover Item", command=remover_item).pack()

    # =========================
    # SALVAR ORÇAMENTO
    # =========================

    def salvar_orcamento():

        cliente_nome = cliente_var.get()
        cliente_escolhido = next(c for c in dados["clientes"] if c["nome"] == cliente_nome)
        total = calcular_total(itens)
        forma_pagamento = entry_pagamento.get()
        prazo_execucao = entry_prazo.get()
        observacoes = entry_obs.get()
        validade = entry_validade.get()

        numero = gerar_numero_orcamento(dados)

        orcamento = {
            
            "numero": numero,  # número correto
            "data": datetime.now().strftime("%d/%m/%Y"),
            "cliente": cliente_escolhido,
            "itens": itens,
            "total": total,
            "forma_pagamento": forma_pagamento,
            "prazo_execucao": prazo_execucao,
            "observacoes": observacoes,
            "validade": validade,
            
        }

        if "orcamentos" not in dados:
            dados["orcamentos"] = []

        dados["orcamentos"].append(orcamento)

        salvar_dados(dados)

        messagebox.showinfo("Sucesso", "Orçamento salvo com sucesso!")  # popup

        janela.destroy()


    tk.Label(janela, text="Forma de pagamento").pack()
    entry_pagamento = tk.Entry(janela)
    entry_pagamento.pack()

    tk.Label(janela, text="Prazo de execução").pack()
    entry_prazo = tk.Entry(janela)
    entry_prazo.pack()

    tk.Label(janela, text="Observações").pack()
    entry_obs = tk.Entry(janela)
    entry_obs.pack()

    tk.Label(janela, text="Validade").pack()
    entry_validade = tk.Entry(janela)
    entry_validade.pack()    

    tk.Button(janela, text="Salvar Orçamento", command=salvar_orcamento).pack(pady=10)

# tela para listar orçamentos
def tela_listar_orcamentos():

    from banco import carregar_dados

    dados = carregar_dados()

    janela = tk.Toplevel()
    janela.title("Orçamentos")
    janela.geometry("500x400")

    tk.Label(janela, text="Lista de Orçamentos", font=("Arial", 14)).pack(pady=10)

    if "orcamentos" not in dados or len(dados["orcamentos"]) == 0:
        tk.Label(janela, text="Nenhum orçamento encontrado").pack()
        return

    for orc in dados["orcamentos"]:
        cliente = orc["cliente"]["nome"]
        total = orc["total"]
        numero = orc.get("numero", "N/A")

        texto = f"{numero} | {cliente} | R$ {total:.2f}"

        tk.Label(janela, text=texto, anchor="w").pack(fill="x", padx=10, pady=2)

def tela_excluir_orcamento():

    from banco import carregar_dados, salvar_dados

    dados = carregar_dados()

    janela = tk.Toplevel()
    janela.title("Excluir Orçamento")
    janela.geometry("500x400")

    tk.Label(janela, text="Selecione um orçamento", font=("Arial", 14)).pack(pady=10)

    if "orcamentos" not in dados or len(dados["orcamentos"]) == 0:
        tk.Label(janela, text="Nenhum orçamento disponível").pack()
        return

    lista = tk.Listbox(janela, width=70)
    lista.pack(pady=10)

    # preencher lista
    for orc in dados["orcamentos"]:
        texto = f"{orc.get('numero','N/A')} | {orc['cliente']['nome']} | R$ {orc['total']:.2f}"
        lista.insert(tk.END, texto)

    def excluir():
        try:
            selecionado = lista.curselection()[0]

            removido = dados["orcamentos"].pop(selecionado)

            salvar_dados(dados)

            messagebox.showinfo("Sucesso", "Orçamento excluído!")

            janela.destroy()

        except:
            messagebox.showwarning("Erro", "Selecione um orçamento!")

    tk.Button(janela, text="Excluir", command=excluir).pack(pady=10)