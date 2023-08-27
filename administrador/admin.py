import requests
import threading
import time
import os
import sys

SERVER_URL = "http://192.168.1.24:8000"

def get_caixas():
    response = requests.get(f"{SERVER_URL}/caixa")
    if response.status_code == 200:
        caixas = response.json()
        for caixa in caixas:
            print(caixa)
    else:
        print("Erro ao recuperar caixas.")

def get_compras():
    response = requests.get(f"{SERVER_URL}/compras")
    if response.status_code == 200:
        compras = response.json()
        for compra in compras:
            print(compra)
    else:
        print("Erro ao recuperar compras.")

def clear_terminal():
    # Detectar o sistema operacional e limpar o terminal de acordo
    os.system('cls' if os.name == 'nt' else 'clear')

def key_pressed_unix():
    import select
    dr, dw, de = select.select([sys.stdin], [], [], 0)
    return dr != []

def key_pressed_windows():
    import msvcrt
    return msvcrt.kbhit()

# Escolhe a função adequada com base no sistema operacional
key_pressed = key_pressed_windows if os.name == 'nt' else key_pressed_unix

def acompanhar_compras_tempo_real():
    print("Acompanhando compras em tempo real. Pressione CTRL+C para interromper.")
    try:
        while True:
            clear_terminal()  # Limpar o terminal
            get_compras()
            if key_pressed():
                break
            time.sleep(5)  # Checa a cada 5 segundos
    except KeyboardInterrupt:
        print("\nAcompanhamento interrompido.")

def criar_caixa():
    try:
        # Coletar as informações do caixa
        caixa_id = input("Informe o ID para o novo caixa: ")

        # Converter o ID para inteiro
        caixa_id_int = int(caixa_id)

        # Criar o objeto JSON para o caixa com status sempre definido como true
        novo_caixa = {
            'id': caixa_id_int,
            'status': True
        }

        # Fazer requisição POST ao servidor para adicionar o caixa
        response = requests.post(f"{SERVER_URL}/caixa", json=novo_caixa)

        if response.status_code == 201:
            print(f"\nCaixa com ID {caixa_id} criado com sucesso!")
        else:
            print("\nErro ao criar caixa. Tente novamente.")
    except ValueError:
        print("O ID informado não é um número válido.")
    except Exception as e:
        print(f"Erro ao criar caixa: {e}")

def bloquear_desbloquear_caixa():
    try:
        get_caixas()

        # Escolher o caixa a ser bloqueado/desbloqueado
        caixa_id_no_int = input("\nInforme o ID do caixa que deseja bloquear ou desbloquear: ")
        
        caixa_id = int(caixa_id_no_int)

        # Obter o status atual do caixa
        response = requests.get(f"{SERVER_URL}/caixa/{caixa_id}")
        
        if response.status_code != 200:
            print(f"\nErro ao obter informações do caixa. Código de status: {response.status_code}. Mensagem: {response.text}")
            return

        caixa_info = response.json()
        atual_status = caixa_info.get('status', None)
        
        if atual_status is None:
            print("\nNão foi possível determinar o status atual do caixa.")
            return

        # Perguntar ao administrador a ação desejada
        if atual_status:
            acao = input(f"O caixa {caixa_id} está desbloqueado. Você deseja bloqueá-lo? (sim/não): ").lower()
            novo_status = False if acao == 'sim' else True
        else:
            acao = input(f"O caixa {caixa_id} está bloqueado. Você deseja desbloqueá-lo? (sim/não): ").lower()
            novo_status = True if acao == 'sim' else False

        # Atualizar o status do caixa com base na escolha do administrador
        if novo_status != atual_status:
            data = {'status': novo_status}
            response = requests.put(f"{SERVER_URL}/caixa/{caixa_id}", json=data)
            if response.status_code == 200:
                if novo_status:
                    print(f"\nCaixa {caixa_id} foi desbloqueado com sucesso!")
                else:
                    print(f"\nCaixa {caixa_id} foi bloqueado com sucesso!")
            else:
                print("\nErro ao atualizar o status do caixa.")
                print("Mensagem do servidor:", response.text)
        else:
            print("\nNenhuma alteração realizada no caixa.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")


def main():
    while True:
        print("\nOpções:")
        print("1: Ver caixas")
        print("2: Ver histórico de compras")
        print("3: Acompanhar compras em tempo real")
        print("4: Criar novo caixa") # Nova opção
        print("5: Bloquear/Desbloquear caixa")
        print("6: Sair")

        escolha = input("\nSelecione uma opção: ")

        if escolha == '1':
            get_caixas()
        elif escolha == '2':
            get_compras()
        elif escolha == '3':
            threading.Thread(target=acompanhar_compras_tempo_real).start()
        elif escolha == '4':
            criar_caixa()
        elif escolha == '6':
            print("\nSaindo...")
            break
        elif escolha == '5':
            bloquear_desbloquear_caixa()
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()
