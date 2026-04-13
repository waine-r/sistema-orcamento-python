from banco import carregar_dados, salvar_dados # Importa funções do banco e clientes
from reportlab.lib.pagesizes import A4  # tamanho da folha
from reportlab.pdfgen import canvas     # ferramenta para criar PDF
from reportlab.lib.utils import ImageReader  # permite usar imagem (logo)
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime # usado para pegar data atual
from colorthief import ColorThief
from calculos import calcular_subtotal, calcular_total  # importa funções de cálculo
from utils import ler_int, ler_float, escolher_opcao  # importa validações

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

    empresa = dados.get("empresa", {})  # pega dados da empresa
    logo_path = empresa.get("logo", None)  # caminho da logo (se existir)


    # Verifica se existem clientes cadastrados
    if "clientes" not in dados or len(dados["clientes"]) == 0:
        print("Você precisa cadastrar um cliente primeiro!")
        return

    print("\n=== NOVO ORÇAMENTO ===")

    # Mostra lista de clientes para escolher
    print("\nSelecione o cliente:")

    for i, cliente in enumerate(dados["clientes"]):
        print(f"{i + 1} - {cliente['nome']}")

   
    escolha = escolher_opcao(dados["clientes"], "Digite o número do cliente: ")
    cliente_escolhido = dados["clientes"][escolha]

    # Lista de itens do orçamento
    itens = []

    while True:
        print("\n=== Adicionar Item ===")

        descricao = input("Descrição do serviço: ")
        unidade = input("Unidade (m², un, m...): ")
        quantidade = ler_float("Quantidade: ")
        valor_unitario = ler_float("Valor unitário: ")

        # Calcula subtotal
        subtotal = calcular_subtotal(quantidade, valor_unitario)  # usa função externa

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
    total = calcular_total(itens)  # usa função externa

        # =========================
    # INFORMAÇÕES ADICIONAIS
    # =========================

    print("\n=== INFORMAÇÕES DO ORÇAMENTO ===")

    forma_pagamento = input("Forma de pagamento: ")
    prazo_execucao = input("Prazo de execução: ")
    observacoes = input("Observações: ")
    validade = input("Validade do orçamento (ex: 15 dias): ")

    # Criando estrutura do orçamento
    # Gera número do orçamento
    numero = gerar_numero_orcamento(dados)

    # Cria o orçamento com número e data
    orcamento = {
        "numero": numero,  # número profissional
        "data": datetime.now().strftime("%d/%m/%Y"),  # data atual
        "cliente": cliente_escolhido,
        "itens": itens,
        "total": total,
        "forma_pagamento": forma_pagamento,
        "prazo_execucao": prazo_execucao,
        "observacoes": observacoes,
        "validade": validade,
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
        for i, item in enumerate(orcamento["itens"]):
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

    escolha = escolher_opcao(dados["orcamentos"], "Digite o número do orçamento que deseja excluir: ")
    
    # Verifica se a escolha é válida
    if escolha < 0 or escolha >= len(dados["orcamentos"]):
        print("Opção inválida.")
        return

    # Remove o orçamento da lista
    removido = dados["orcamentos"].pop(escolha)

    # Salva os dados atualizados
    salvar_dados(dados)

    print(f"Orçamento do cliente {removido['cliente']['nome']} excluído com sucesso!")

def gerar_pdf_orcamento(indice=None):

    from banco import carregar_dados
    import webbrowser
    import os

    dados = carregar_dados()

    empresa = dados.get("empresa", {})
    logo_path = empresa.get("logo", None)

    # define cor dinâmica
    if logo_path:
        cor_principal = pegar_cor_logo(logo_path)
    else:
        cor_principal = colors.HexColor("#2E7D32")  # fallback

    if "orcamentos" not in dados or len(dados["orcamentos"]) == 0:
        print("Nenhum orçamento encontrado.")
        return

    # 👉 SE NÃO VEIO ÍNDICE → usa input (modo antigo)
    if indice is None:
        for i, orc in enumerate(dados["orcamentos"]):
            print(f"{i + 1} - {orc['cliente']['nome']} - R$ {orc['total']}")

        escolha = int(input("Escolha o orçamento: ")) - 1

    else:
        escolha = indice  # usa índice da interface

    if escolha < 0 or escolha >= len(dados["orcamentos"]):
        print("Opção inválida.")
        return

    orcamento = dados["orcamentos"][escolha]


# Verifica se existem orçamentos
    if "orcamentos" not in dados or len(dados["orcamentos"]) == 0:
        print("Nenhum orçamento encontrado.")
        return

    # Nome do arquivo PDF
    nome_arquivo = f"orcamento_{orcamento.get('numero','sem_numero')}.pdf"

    # Cria o PDF
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4
    margem_esquerda = 40
    margem_direita = largura - 40

        # =========================
    # GRID DO DOCUMENTO
    # =========================

    margem_esquerda = 40
    margem_direita = largura - 40

    # largura útil (sem faixa direita)
    largura_util = largura - 120

    # colunas base
    col_esquerda = margem_esquerda
    col_meio = margem_esquerda + (largura_util * 0.5)
    col_direita = margem_esquerda + largura_util

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

    x_info = col_meio

    c.drawString(x_info, y_topo, empresa.get("nome", ""))
    c.drawString(x_info, y_topo - 15, f"CNPJ: {empresa.get('cnpj', '')}")
    c.drawString(x_info, y_topo - 30, f"Telefone: {empresa.get('telefone', '')}")
    c.drawString(x_info, y_topo - 45, f"Endereço: {empresa.get('endereco', '')}")

    # =========================
    # LINHA SEPARADORA
    # =========================

    c.setStrokeColor(cor_principal)
    c.setLineWidth(2)

    c.setStrokeColor(cor_principal)
    c.setLineWidth(2)

    c.line(margem_esquerda, 720, margem_direita, 720)
    c.setStrokeColor(colors.black)


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

    c.drawString(col_esquerda, 690, titulo)
    
    c.setFillColor(colors.black)  # volta ao normal

    c.setFont("Helvetica", 11)

# =========================
# CAIXA CLIENTE
# =========================

    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)

    # desenha a caixa
    c.rect(col_esquerda, 610, largura - 120, 70)                
        
        
        # =========================
    # BLOCO CLIENTE
    # =========================

    y = 665  # posição inicial

    c.setFont("Helvetica", 11)

    c.drawString(44, y, f"Cliente: {orcamento['cliente']['nome']}")
    y -= 15

    c.drawString(44, y, f"Telefone: {orcamento['cliente']['telefone']}")
    y -= 15

    c.drawString(44, y, f"Email: {orcamento['cliente']['email']}")
    y -= 15

    c.drawString(44, y, f"Endereço: {orcamento['cliente']['endereco']}")
    y -= 25  # espaço maior antes da mensagem

    c.setFont("Helvetica", 10)

        # =========================
    # MENSAGEM
    # =========================

    c.setFont("Helvetica", 10)

    c.drawString(col_esquerda, y, "Prezado (a) Sr (a),")
    y -= 15

    c.drawString(col_esquerda, y, "Agradecemos pela oportunidade de apresentar nosso orçamento.")
    y -= 15

    c.drawString(col_esquerda, y, "Estamos à disposição para quaisquer dúvidas ou ajustes necessários.")
    y -= 25

    # =========================
    # TABELA
    # =========================

        # Título da tabela
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col_esquerda, y, "Itens do orçamento:")
    y -= 20

    c.setFont("Helvetica", 10)

    # Dados da tabela
    dados_tabela = [["Serviço", "Qtd", "Unidade", "V. Unitário", "Total"]]

    for i, item in enumerate(orcamento["itens"]):
        dados_tabela.append([
            item["descricao"],
            formatar_numero(item["quantidade"]),
            item["unidade"],
            formatar_moeda(item['valor_unitario']),
            formatar_moeda(item['subtotal'])
        ])

    # =========================
# LARGURA SEGURA DA TABELA
# =========================

    largura_util = largura - 120  # espaço da página menos margem + faixa

        # =========================
    # TABELA MANUAL (COM QUEBRA)
    # =========================

    y_tabela = y - 10  # começa abaixo do título

    c.setFont("Helvetica", 10)

    # Cabeçalho
    c.setFillColor(cor_principal)
    c.rect(col_esquerda, y_tabela, largura_util, 20, fill=1)

    c.setFillColor(colors.white)
    c.drawString(col_esquerda + 5, y_tabela + 5, "Serviço")
    c.drawString(col_esquerda + 180, y_tabela + 5, "Qtd")
    c.drawString(col_esquerda + 230, y_tabela + 5, "Unidade")
    c.drawString(col_esquerda + 300, y_tabela + 5, "V. Unitário")
    c.drawString(col_esquerda + 400, y_tabela + 5, "Total")

    y_tabela -= 20

        # segurança: garante que começa em posição válida
    if y_tabela < 200:
        y_tabela = altura - 150

    for i, item in enumerate(orcamento["itens"]):

        c.setFillColor(colors.black)  # 🔥 reset ANTES de tudo

        # 🔥 verifica se chegou no fim da página
        if y_tabela < 150:
            c.showPage()

                        # =========================
            # BORDA LATERAL (RECRIAR)
            # =========================

            c.setFillColor(cor_principal)

            # faixa lateral
            c.rect(largura - 80, 0, 80, altura, fill=1)

            # círculo branco
            c.setFillColor(colors.white)

            c.circle(
                largura,
                altura / 2,
                200,
                fill=1,
                stroke=0
            )

             # =========================
            # RECRIA HEADER
            # =========================

            y_topo = 800

            #LOGO
            if logo_path:
                try:
                    logo = ImageReader(logo_path)
                    c.drawImage(
                        logo,
                        0,
                        y_topo - 70,
                        width=220,
                        height=110,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
                except:
                    pass

            # 🔥 IMPORTANTE: reset de cor e fonte
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 10)

            #DADOS DA EMPRESA
            c.drawString(col_meio, y_topo, empresa.get("nome", ""))
            c.drawString(col_meio, y_topo - 15, f"CNPJ: {empresa.get('cnpj', '')}")
            c.drawString(col_meio, y_topo - 30, f"Telefone: {empresa.get('telefone', '')}")
            c.drawString(col_meio, y_topo - 45, f"Endereço: {empresa.get('endereco', '')}")

            #LINHA HEADER
            c.setStrokeColor(cor_principal)
            c.setLineWidth(2)
            c.line(margem_esquerda, 720, margem_direita, 720)

            c.setStrokeColor(colors.black)  # 🔥 CORREÇÃO DEFINITIVA

            # =========================
            # RECRIA CABEÇALHO DA TABELA
            # =========================

            y_tabela = 680

            c.setFillColor(cor_principal)
            c.rect(col_esquerda, y_tabela, largura_util, 20, fill=1)

            c.setFillColor(colors.white)

            c.drawString(col_esquerda + 5, y_tabela + 5, "Serviço")
            c.drawString(col_esquerda + 180, y_tabela + 5, "Qtd")
            c.drawString(col_esquerda + 230, y_tabela + 5, "Unidade")
            c.drawString(col_esquerda + 300, y_tabela + 5, "V. Unitário")
            c.drawString(col_esquerda + 400, y_tabela + 5, "Total")

            c.setFillColor(colors.black)  # 🔥 reset obrigatório  
            y_tabela -= 20

                    # =========================
        # 🔥 FUNDO ZEBRA (AQUI)
        # =========================
        # volta para texto
        c.setFillColor(colors.black)

        # =========================
        # 🔥 AQUI FICAM SEUS drawString
        # =========================

        c.drawString(col_esquerda + 5, y_tabela, item["descricao"])
        c.drawString(col_esquerda + 180, y_tabela, formatar_numero(item["quantidade"]))
        c.drawString(col_esquerda + 230, y_tabela, item["unidade"])
        c.drawString(col_esquerda + 300, y_tabela, formatar_moeda(item["valor_unitario"]))
        c.drawString(col_esquerda + 400, y_tabela, formatar_moeda(item["subtotal"]))

        # =========================
        # 🔥 LINHA SEPARADORA (AQUI)
        # =========================
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.5)
        c.line(col_esquerda, y_tabela - 5, col_direita, y_tabela - 5)

        y_tabela -= 20


    # limite visual à direita (segurança)
    limite_direito = largura - 100

        # Caixa de destaque do total
    pos_y_total = y_tabela - 30

    # =========================
# TOTAL ALINHADO NO GRID
# =========================

    largura_total_box = 170

    x_total = col_direita - largura_total_box  # 🔥 alinha com grid

    c.setFillColor(cor_principal)
    c.rect(x_total, pos_y_total, largura_total_box, 35, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)

    c.drawRightString(
        col_direita - 10,  # 🔥 alinhado com borda do grid
        pos_y_total + 10,
        f"TOTAL: {formatar_moeda(orcamento['total'])}"
    )

    print("Logo path:", logo_path)
    
    # =========================
# INFORMAÇÕES DO ORÇAMENTO
# =========================

    y_info = pos_y_total - 40  # começa abaixo do total

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)

    c.drawString(50, y_info, f"Forma de pagamento: {orcamento.get('forma_pagamento', '')}")
    y_info -= 15

    c.drawString(50, y_info, f"Prazo de execução: {orcamento.get('prazo_execucao', '')}")
    y_info -= 15

    c.drawString(50, y_info, f"Observações: {orcamento.get('observacoes', '')}")
    y_info -= 15

    c.drawString(50, y_info, f"Validade do orçamento: {orcamento.get('validade', '')}")
    
    # =========================
# RODAPÉ
# =========================

    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)

    # linha separadora
    c.setStrokeColor(cor_principal)  # mesma cor do header
    c.setLineWidth(2)                # mesma espessura

    c.line(margem_esquerda, 100, margem_direita, 100)

    # texto do rodapé
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)

    cidade = "Juiz de Fora"  # depois podemos puxar automático

    c.drawString(50, 80, f"{cidade}, {orcamento.get('data', '')}")
           
        
        
        # =========================
    # FINALIZAÇÃO DO PDF
    # =========================

    c.save()

    import webbrowser  # abre no navegador padrão
    import os

    nome_arquivo = f"orcamento_{orcamento.get('numero','sem_numero')}.pdf"

    caminho = os.path.abspath(nome_arquivo)

    webbrowser.open(f"file://{caminho}")

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
