import json
import os
import sys  # usado para detectar se é .exe

# 🔥 verifica se está rodando como .exe
if getattr(sys, 'frozen', False):
    # quando for .exe → usa a pasta do executável
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # quando for Python normal → usa a pasta do arquivo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# caminho do banco de dados (arquivo JSON)
CAMINHO_ARQUIVO = os.path.join(BASE_DIR, "dados.json")

# função para carregar dados do JSON
def carregar_dados():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return {}

    with open(CAMINHO_ARQUIVO, "r") as arquivo:
        return json.load(arquivo)

# função para salvar dados no JSON
def salvar_dados(dados):
    with open(CAMINHO_ARQUIVO, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

# Define o caminho correto do dados.json dentro da pasta do projeto
CAMINHO_ARQUIVO = os.path.join(BASE_DIR, "dados.json")


def carregar_dados():
    # Se não existir, retorna vazio
    if not os.path.exists(CAMINHO_ARQUIVO):
        return {}

    with open(CAMINHO_ARQUIVO, "r") as arquivo:
        return json.load(arquivo)


def salvar_dados(dados):
    with open(CAMINHO_ARQUIVO, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)