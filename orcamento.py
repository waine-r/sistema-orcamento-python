from banco import carregar_dados, salvar_dados # Importa funções do banco e clientes
from reportlab.lib.pagesizes import A4  # tamanho da folha
from reportlab.pdfgen import canvas     # ferramenta para criar PDF
from reportlab.lib.utils import ImageReader  # permite usar imagem (logo)
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime # usado para pegar data atual
from colorthief import ColorThief


def gerar_numero_orcamento(dados):
    """
    Gera número no formato:
    XXYY.AAAA

    XX = quantidade de orçamentos no mês atual
    YY = mês
    AAAA = ano
    """

    # Pega data atual
    agora = datetime.now()
    ano = agora.year
    mes = agora.month

    # Se não existir orçamento ainda
    if "orcamentos" not in dados:
        quantidade_mes = 1
    else:
        quantidade_mes = 0

        # Percorre todos os orçamentos já salvos
        for orc in dados["orcamentos"]:
            data = orc.get("data")

            # Se existir data salva
            if data:
                data_orc = datetime.strptime(data, "%d/%m/%Y")

                # Verifica se é do mesmo mês e ano
                if data_orc.month == mes and data_orc.year == ano:
                    quantidade_mes += 1

        # Soma +1 para o novo orçamento
        quantidade_mes += 1

    # Formata número final
    return f"{quantidade_mes:02d}{mes:02d}.{ano}"

cor_principal = colors.HexColor("#2E7D32")  # verde profissional

# Função para criar um novo orçamento
def criar_orcamento():
    dados = carregar_dados()


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
    # Gera número do orçamento
    numero = gerar_numero_orcamento(dados)

    # Cria o orçamento com número e data
    orcamento = {
        "numero": numero,  # número profissional
        "data": datetime.now().strftime("%d/%m/%Y"),  # data atual
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

    # Pegar dados da empresa
    empresa = dados.get("empresa", {})
    logo_path = empresa.get("logo")
    # Define cor baseada na logo
    cor_principal = pegar_cor_logo(logo_path) if logo_path else colors.HexColor("#2E7D32")
    # Remove aspas caso existam
    if logo_path:
        logo_path = logo_path.replace('"', '')


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

    # =========================
    # HEADER PROFISSIONAL
    # =========================

    y_topo = 800

        # LOGO MAIOR (mais à esquerda)
    if logo_path:
        try:
            logo = ImageReader(logo_path)
            c.drawImage(
                logo,
                0,              # mais à esquerda
                y_topo - 70,     # um pouco mais baixo
                width=220,       # 🔥 maior
                height=110,
                preserveAspectRatio=True,
                mask='auto'
            )
        except Exception as e:
            print("Erro logo:", e)

    # DADOS MAIS À DIREITA
    c.setFont("Helvetica", 10)

    x_info = 250  # 🔥 joga mais para direita

    c.drawString(x_info, y_topo, empresa.get("nome", ""))
    c.drawString(x_info, y_topo - 15, f"CNPJ: {empresa.get('cnpj', '')}")
    c.drawString(x_info, y_topo - 30, f"Telefone: {empresa.get('telefone', '')}")
    c.drawString(x_info, y_topo - 45, f"Endereço: {empresa.get('endereco', '')}")

    # =========================
    # LINHA SEPARADORA
    # =========================

    c.setStrokeColor(cor_principal)
    c.setLineWidth(2)

    c.line(40, 720, largura - 40, 720)


    # =========================
    # BORDA LATERAL
    # =========================

    c.setFillColor(cor_principal)

   # Forma curva simples
    c.setFillColor(cor_principal)

        # =========================
    # BORDA MODERNA (2 cores)
    # =========================

    # Cor principal
    c.setFillColor(cor_principal)

    # Faixa principal
    c.rect(largura - 80, 0, 80, altura, fill=1)

    # Segunda cor (mais clara)
    # =========================
# CÍRCULO BRANCO (recorte)
# =========================

    c.setFillColor(colors.white)  # 🔥 branco igual fundo

    c.circle(
        largura,          # encostado na direita
        altura / 2,       # centralizado verticalmente
        200,              # tamanho da bola
        fill=1,
        stroke=0          # 🔥 sem borda
    )

 

    # Título
    c.setFillColor(cor_principal)
    c.setFont("Helvetica-Bold", 18)
    
        # Número e data do orçamento
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)

    c.setFillColor(cor_principal)
    c.setFont("Helvetica-Bold", 18)

    # Junta título + número
    titulo = f"ORÇAMENTO {orcamento.get('numero', '')}"    

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(cor_principal)

    c.drawString(50, 690, titulo)
    
    c.setFillColor(colors.black)  # volta ao normal

    c.setFont("Helvetica", 11)

# =========================
# CAIXA CLIENTE
# =========================

    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)

    # desenha a caixa
    c.rect(40, 610, largura - 120, 70)                
        
        
        # =========================
    # BLOCO CLIENTE
    # =========================

    y = 665  # posição inicial

    c.setFont("Helvetica", 11)

    c.drawString(50, y, f"Cliente: {orcamento['cliente']['nome']}")
    y -= 15

    c.drawString(50, y, f"Telefone: {orcamento['cliente']['telefone']}")
    y -= 15

    c.drawString(50, y, f"Email: {orcamento['cliente']['email']}")
    y -= 15

    c.drawString(50, y, f"Endereço: {orcamento['cliente']['endereco']}")
    y -= 25  # espaço maior antes da mensagem

    c.setFont("Helvetica", 10)

        # =========================
    # MENSAGEM
    # =========================

    c.setFont("Helvetica", 10)

    c.drawString(50, y, "Prezado cliente,")
    y -= 15

    c.drawString(50, y, "Agradecemos pela oportunidade de apresentar nosso orçamento.")
    y -= 15

    c.drawString(50, y, "Estamos à disposição para quaisquer dúvidas ou ajustes necessários.")
    y -= 25

    # =========================
    # TABELA
    # =========================

        # Título da tabela
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Itens do orçamento:")
    y -= 20

    c.setFont("Helvetica", 10)

    # Dados da tabela
    dados_tabela = [["Serviço", "Qtd", "Unidade", "V. Unitário", "Total"]]

    for item in orcamento["itens"]:
        dados_tabela.append([
            item["descricao"],
            formatar_numero(item["quantidade"]),
            item["unidade"],
            formatar_moeda(item['valor_unitario']),
            formatar_moeda(item['subtotal'])
        ])

    tabela = Table(dados_tabela, colWidths=[180, 50, 60, 100, 100])

    tabela.setStyle(TableStyle([
    # Cabeçalho
    ('BACKGROUND', (0,0), (-1,0), cor_principal),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    # Alinhamento das colunas
    ('ALIGN', (1,1), (2,-1), 'CENTER'),   # quantidade + unidade
    ('ALIGN', (3,1), (-1,-1), 'RIGHT'),   # valores à direita

    # Linhas
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),

]))
    
    tabela.wrapOn(c, largura, altura)
    tabela.drawOn(c, 50, y - 120)

        # Caixa de destaque do total
    pos_y_total = y - 160

    c.setFillColor(cor_principal)
    c.rect(330, pos_y_total, 170, 35, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawRightString(
    490,
    pos_y_total + 10,
    f"TOTAL: {formatar_moeda(orcamento['total'])}"
)

    print("Logo path:", logo_path)

        # =========================
    # FINALIZAÇÃO DO PDF
    # =========================

    c.save()

    print(f"PDF gerado com sucesso: {nome_arquivo}")

def pegar_cor_logo(caminho_logo):
    """
    Extrai a cor principal da logo
    """
    try:
        color_thief = ColorThief(caminho_logo)
        r, g, b = color_thief.get_color(quality=1)

        # Converte para padrão do reportlab (0 a 1)
        return colors.Color(r/255, g/255, b/255)

    except:
        # fallback (verde padrão)
        return colors.HexColor("#2E7D32")

def formatar_moeda(valor):
    """
    Converte 22500.00 → R$ 22.500,00
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_numero(valor):
    """
    Converte 150.0 → 150,00
    """
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

