# Importa funções dos outros arquivos
from empresa import cadastrar_empresa
from cliente import cadastrar_cliente, listar_clientes
from orcamento import criar_orcamento
from orcamento import listar_orcamentos
from orcamento import excluir_orcamento
from orcamento import gerar_pdf_orcamento


# Função principal que controla o menu
def menu():
    # Loop infinito (continua rodando até escolher sair)
    while True:
        print("1 - Cadastrar empresa")
        print("2 - Cadastrar cliente")
        print("3 - Listar clientes")
        print("4 - Criar orçamento")
        print("5 - Listar orçamentos")
        print("6 - Excluir orçamento")
        print("7 - Gerar PDF")
        print("8 - Sair")

        # Recebe a opção do usuário
        opcao = input("Escolha uma opção: ")

        # Verifica qual opção foi escolhida
        if opcao == "1":
            cadastrar_empresa()

        elif opcao == "2":
            cadastrar_cliente()

        elif opcao == "3":
            listar_clientes()

        elif opcao == "4":
            criar_orcamento()

        elif opcao =="5":
            listar_orcamentos()

        elif opcao == "6":
            excluir_orcamento()

        elif opcao == "7":
            gerar_pdf_orcamento()

        elif opcao == "8":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


# Inicia o programa
menu()