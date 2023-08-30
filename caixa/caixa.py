import json
import requests
import socket
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from ipconfig import hostip, port, server_host

def realizar_compra():
    produtos = []
    
    while True:
        print("\nInforme os detalhes do produto ou digite 'sair' para finalizar a compra.")
        
        nome = input("Nome do produto: ")
        if nome.lower() == 'sair':
            break
        
        preco = float(input("Preço do produto: "))
        quantidade = int(input("Quantidade: "))

        produto = {
            'nome': nome,
            'preco': preco,
            'quantidade': quantidade
        }
        
        produtos.append(produto)

    return produtos

def pegar_produtos_do_sensor():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto('Olá, servidor!'.encode('utf-8'), ("192.168.1.24", 8000))

    data, server_address = client_socket.recvfrom(1024)
    produtos = json.loads(data.decode('utf-8'))

    print("\nProdutos adquiridos do sensor:")
    for produto in produtos:
        print(f"Nome: {produto['nome']}, Preço: {produto['preco']}")
        
    return produtos

def exibir_carrinho(compras):
    total = 0
    print("\nItens no Carrinho:")
    for produto in compras:
        print(f"Nome: {produto['nome']}, Preço: {produto['preco']:.2f}, Quantidade: {produto['quantidade']}")
        total += produto['preco'] * produto['quantidade']
    
    print(f"\nTotal a Pagar: {total:.2f}")
    return total

def pagar_compra(total):
    print(f"\nTotal da Compra: {total:.2f}")
    pago = float(input("Informe o valor pago: "))
    
    if pago >= total:
        troco = pago - total
        print(f"\nTroco: {troco:.2f}")
        return True
    else:
        print("\nValor insuficiente.")
        return False

def escolher_caixa():
    response = requests.get(server_host+"caixa")
    if response.status_code == 200:
        caixas = response.json()
        
        # Filtrando caixas disponíveis
        caixas_disponiveis = [caixa for caixa in caixas if caixa.get('status', False)]
        
        # Se todos os caixas estiverem bloqueados
        if not caixas_disponiveis:
            print("\nTodos os caixas estão bloqueados no momento.")
            return None
        
        ids_disponiveis = [caixa["id"] for caixa in caixas_disponiveis]
        
        print("\nCAIXAS DISPONÍVEIS ID:", ", ".join(map(str, ids_disponiveis)))
        
        while True:
            try:
                escolha = int(input("Escolha qual caixa para iniciar: "))
                caixa_escolhido = next((caixa for caixa in caixas_disponiveis if caixa['id'] == escolha), None)
                
                if caixa_escolhido:
                    if not caixa_escolhido.get('status', False):
                        print("\nO caixa selecionado está bloqueado. Escolha outro.")
                    else:
                        return escolha
                else:
                    print("\nID de caixa inválido. Tente novamente.")
            except ValueError:
                print("\nPor favor, insira um número válido para o ID do caixa.")
    else:
        print("Erro ao recuperar caixas.")
        return None

def main():
    id_caixa = escolher_caixa()
    print(f"\nVocê escolheu o caixa com ID: {id_caixa}")
    
    compras = []
    while True:
        print("\nOpções:")
        print("1: Adicionar produto à compra manualmente")
        print("2: Pegar produtos do sensor")
        print("3: Verificar itens no carrinho")
        print("4: Pagar compra")
        print("5: Sair")

        escolha = input("\nSelecione uma opção: ")

        if escolha == '1':
            compras += realizar_compra()
        elif escolha == '2':
            produtos_sensor = pegar_produtos_do_sensor()
            compras += produtos_sensor
        elif escolha == '3':
            exibir_carrinho(compras)
        elif escolha == '4':
            total = exibir_carrinho(compras)
            if pagar_compra(total):
                response = requests.post(server_host+"compras", json=compras)
                
                if response.status_code == 201:
                    print("\nCompra realizada com sucesso!")
                    compras = []
                else:
                    print("\nErro ao realizar compra.")
        elif escolha == '5':
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()
