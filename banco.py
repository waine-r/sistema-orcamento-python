import json
import os

# Pega o caminho da pasta onde está este arquivo (banco.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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