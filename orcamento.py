from banco import carregar_dados, salvar_dados # Importa funções do banco e clientes
from reportlab.lib.pagesizes import A4  # tamanho da folha
from reportlab.pdfgen import canvas     # ferramenta para criar PDF

# Função para gerar PDF de um orçamento


def gerar_pdf_orcamento():
    dados = carregar_dados()

# Função para criar um novo orçamento
def criar_orcamento():
    dados = carregar_dados()

    print("DEBUG dados:", dados)

    # Verifica se existem clientes cadastrados
    if "clientes" not in dados or len(dados["clientes"]) == 0:
        print("Você precisa cadastrar um cliente primeiro!")
        return

    print("\n=== NOVO ORÇAMENTO ===")

    # Mostra lista de clientes para escolher
    print("\nSelecione o cliente:")

    for i, cliente in enumerate(dados["clientes"]):
        print(f"{i + 1} - {cliente['nome']}")

    # Usuário escolhe cliente
    escolha = int(input("Digite o número do cliente: ")) - 1

    cliente_escolhido = dados["clientes"][escolha]

    # Lista de itens do orçamento
    itens = []

    while True:
        print("\n=== Adicionar Item ===")

        descricao = input("Descrição do serviço: ")
        unidade = input("Unidade (m², un, m...): ")
        quantidade = float(input("Quantidade: "))
        valor_unitario = float(input("Valor unitário: "))

        # Calcula subtotal
        subtotal = quantidade * valor_unitario

        item = {
            "descricao": descricao,
            "unidade": unidade,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
            "subtotal": subtotal
        }

        itens.append(item)

        continuar = input("Adicionar outro item? (s/n): ")

        if continuar.lower() != "s":
            break

    # Cálculo do total
    total = sum(item["subtotal"] for item in itens)

    # Criando estrutura do orçamento
    orcamento = {
        "cliente": cliente_escolhido,
        "itens": itens,
        "total": total
    }

    # Se não existir lista de orçamentos, cria
    if "orcamentos" not in dados:
        dados["orcamentos"] = []

    # Salva o orçamento
    dados["orcamentos"].append(orcamento)

    salvar_dados(dados)

    print("\nOrçamento criado com sucesso!")
    print(f"Valor total: R$ {total:.2f}")

    # Função para listar todos os orçamentos
def listar_orcamentos():
    dados = carregar_dados()

    # Verifica se existem orçamentos
    if "orcamentos" not in dados or len(dados["orcamentos"]) == 0:
        print("Nenhum orçamento encontrado.")
        return

    print("\n=== LISTA DE ORÇAMENTOS ===")

    # Percorre todos os orçamentos
    for i, orcamento in enumerate(dados["orcamentos"]):
        cliente = orcamento["cliente"]["nome"]
        total = orcamento["total"]

        print(f"\nOrçamento {i + 1}")
        print(f"Cliente: {cliente}")
        print(f"Total: R$ {total:.2f}")

        print("Itens:")

        # Percorre os itens do orçamento
        for item in orcamento["itens"]:
            print(f"- {item['descricao']} | {item['quantidade']} {item['unidade']} | R$ {item['subtotal']:.2f}")

# Função para excluir um orçamento
def excluir_orcamento():
    dados = carregar_dados()

    # Verifica se existem orçamentos
    if "orcamentos" not in dados or len(dados["orcamentos"]) == 0:
        print("Nenhum orçamento para excluir.")
        return

    print("\n=== EXCLUIR ORÇAMENTO ===")

    # Mostra lista de orçamentos
    for i, orcamento in enumerate(dados["orcamentos"]):
        cliente = orcamento["cliente"]["nome"]
        total = orcamento["total"]

        print(f"{i + 1} - {cliente} | R$ {total:.2f}")
        print("\nDigite o número do orçamento e pressione ENTER")

    # Usuário escolhe qual excluir
    escolha = int(input("Digite o número do orçamento que deseja excluir: ")) - 1

    # Verifica se a escolha é válida
    if escolha < 0 or escolha >= len(dados["orcamentos"]):
        print("Opção inválida.")
        return

    # Remove o orçamento da lista
    removido = dados["orcamentos"].pop(escolha)

    # Salva os dados atualizados
    salvar_dados(dados)

    print(f"Orçamento do cliente {removido['cliente']['nome']} excluído com sucesso!")

def gerar_pdf_orcamento():
    

    dados = carregar_dados()


# Verifica se existem orçamentos
    if "orcamentos" not in dados or len(dados["orcamentos"]) == 0:
        print("Nenhum orçamento encontrado.")
        return

    print("\n=== GERAR PDF ===")

    # Lista os orçamentos
    for i, orcamento in enumerate(dados["orcamentos"]):
        cliente = orcamento["cliente"]["nome"]
        total = orcamento["total"]

        print(f"{i + 1} - {cliente} | R$ {total:.2f}")

    escolha = int(input("Escolha o orçamento: ")) - 1

    if escolha < 0 or escolha >= len(dados["orcamentos"]):
        print("Opção inválida.")
        return

    orcamento = dados["orcamentos"][escolha]

    # Nome do arquivo PDF
    nome_arquivo = f"orcamento_{escolha + 1}.pdf"

    # Cria o PDF
    c = canvas.Canvas(nome_arquivo, pagesize=A4)

    largura, altura = A4

    y = altura - 50  # posição inicial no topo

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "ORÇAMENTO")
    y -= 30

    # Dados da empresa (se existir)
    if "empresa" in dados:
        empresa = dados["empresa"]

        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Empresa: {empresa['nome']}")
        y -= 15
        c.drawString(50, y, f"CNPJ: {empresa['cnpj']}")
        y -= 15
        c.drawString(50, y, f"Telefone: {empresa['telefone']}")
        y -= 20

    # Dados do cliente
    cliente = orcamento["cliente"]

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Cliente:")
    y -= 15

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Nome: {cliente['nome']}")
    y -= 15
    c.drawString(50, y, f"Telefone: {cliente['telefone']}")
    y -= 20

    # Itens
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Itens:")
    y -= 15

    c.setFont("Helvetica", 10)

    for item in orcamento["itens"]:
        texto = f"{item['descricao']} - {item['quantidade']} {item['unidade']} - R$ {item['subtotal']:.2f}"
        c.drawString(50, y, texto)
        y -= 15

    y -= 10

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"TOTAL: R$ {orcamento['total']:.2f}")

    # Salva o PDF
    c.save()

    print(f"PDF gerado com sucesso: {nome_arquivo}")