import json
import requests
import socket
import sys
import os
import time

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from ipconfigcaixa import hostip, port, server_host

def clear_terminal():
    # Detectar o sistema operacional e limpar o terminal de acordo
    os.system('cls' if os.name == 'nt' else 'clear')

def atualizar_estoque(nome_produto, quantidade_real):
    try:
        response = requests.put(f"{server_host}produtos/{nome_produto}", json={'quantidade': quantidade_real})
        if response.status_code != 200:
            print(f"Erro ao atualizar o estoque do produto com nome {nome_produto}.")
    except Exception as e:
        print(f"Erro ao atualizar o estoque: {e}")

def realizar_compra():
    try:
        response = requests.get(server_host + "produtos")
        if response.status_code != 200:
            print("Não foi possível recuperar a lista de produtos.")
            return []

        produtos_disponiveis = response.json()
        print("\nProdutos disponíveis:")
        for idx, produto in enumerate(produtos_disponiveis):
            print(f"[{idx+1}] Nome: {produto['nome']}, Preço: {produto['preco']}, Quantidade Disponível: {produto['quantidade']}")
    except Exception as e:
        print(f"Erro ao buscar lista de produtos: {e}")
        return []

    produtos_selecionados = []
    while True:
        print("\nSelecione um produto pelo número ou digite 'sair' para finalizar a compra.")
        escolha = input("Escolha: ")

        if escolha.lower() == 'sair':
            break

        try:
            escolha = int(escolha) - 1
            if escolha < 0 or escolha >= len(produtos_disponiveis):
                print("Número de produto inválido.")
                continue

            produto_escolhido = produtos_disponiveis[escolha]
            quantidade = int(input(f"Quantidade de {produto_escolhido['nome']}: "))

            if quantidade > produto_escolhido['quantidade']:
                print("Quantidade indisponível.")
                continue

            # Atualize a quantidade do produto no servidor


            produtos_selecionados.append({
                'nome': produto_escolhido['nome'],
                'preco': produto_escolhido['preco'],
                'quantidade': quantidade
            })
        except ValueError:
            print("Por favor, insira um número válido.")

    return produtos_selecionados


def pegar_produtos_do_sensor():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)  # Define um timeout de 10 segundos
        client_socket.connect(('172.16.103.0', 7777))

        data = client_socket.recv(2048)
        if not data:  # Verificar se não recebeu dados (pode adicionar esta checagem se quiser)
            print("Nenhum dado recebido do sensor.")
            return []

        produtos = json.loads(data.decode('utf-8'))

        print("\nProdutos adquiridos do sensor:")
        for produto in produtos:
            print(f"Nome: {produto['nome']}, Preço: {produto['preco']}")

            # Descontar o produto do estoque
            try:
                response = requests.get(f"{server_host}produtos/{produto['nome']}")
                if response.status_code == 200:
                    produto_servidor = response.json()
                else:
                    print(f"Produto {produto['nome']} não encontrado no estoque.")
            except Exception as e:
                print(f"Erro ao atualizar o estoque do produto {produto['nome']}: {e}")

        client_socket.close()
        return produtos
    except socket.timeout:
        print("Tempo limite da conexão excedido.")
        return []
    except Exception as e:
        print(f"Erro ao pegar produtos do sensor: {e}")
        return []

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
            clear_terminal()
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

def verificar_status_caixa(id_caixa):
    try:
        response = requests.get(f"{server_host}caixa/{id_caixa}")
        if response.status_code == 200:
            caixa = response.json()
            if not caixa.get('status', False):
                print("\nCAIXA BLOQUEADO PELO ADMINISTRADOR")
                return False
            return True
        else:
            print("\nErro ao verificar status do caixa.")
            return False
    except Exception as e:
        print(f"Erro ao verificar status do caixa: {e}")
        return False


def main():
    id_caixa = escolher_caixa()
    
    if id_caixa is None:
        print("Nenhum caixa disponível. Entre em contato com o administrador.")
        return  # Termina o programa se não houver caixas disponíveis
    clear_terminal()
    print(f"\nVocê escolheu o caixa com ID: {id_caixa} entrando no caixa...")
    time.sleep(3)
    clear_terminal()
    
    compras = []
    while True:
        if not verificar_status_caixa(id_caixa):
            print("Ação cancelada devido ao caixa estar bloqueado.")
            break
        print('-------Caixa Supermercado gambiarra--------')
        print("\nOpções:")
        print("[1]: Adicionar produto à compra manualmente")
        print("[2]: Pegar produtos do leitor")
        print("[3]: Verificar itens no carrinho")
        print("[4]: Pagar compra")
        print("[5]: Sair")
        print('-------------------------------------------')

        escolha = input("\nSelecione uma opção: ")

        if escolha == '1':
            compras += realizar_compra()
        elif escolha == '2':
            produtos_sensor = pegar_produtos_do_sensor()
            compras += produtos_sensor
        elif escolha == '3':
            exibir_carrinho(compras)
        elif escolha == '4':
            # Verificando se há estoque suficiente antes de finalizar a compra
            estoque_suficiente = True
            for produto in compras:
                nome_produto = produto['nome']
                quantidade_comprada = produto['quantidade']
                
                # Obtendo a quantidade atual do produto no estoque
                response = requests.get(f"{server_host}produtos/{nome_produto}")
                if response.status_code == 200:
                    produto_servidor = response.json()
                    quantidade_real = produto_servidor['quantidade']
                    
                    if quantidade_real == 0:
                        print(f"Compra não pode ser realizada, {nome_produto} está fora de estoque.")
                        estoque_suficiente = False
                        break
                    elif quantidade_comprada > quantidade_real:
                        print(f"Compra não pode ser realizada, quantidade de {nome_produto} no estoque é insuficiente.")
                        estoque_suficiente = False
                        break
                else:
                    print(f"Erro ao obter informações de estoque para {nome_produto}.")
                    estoque_suficiente = False
                    break
                    
            if not estoque_suficiente:
                continue  # Volta para o menu principal se o estoque for insuficiente

            # Se chegou até aqui, significa que há estoque suficiente
            total = exibir_carrinho(compras)
            if pagar_compra(total):
                response = requests.post(server_host+"compras", json=compras)
                
                if response.status_code == 201:
                    print("\nCompra realizada com sucesso!")
                    
                    # Atualizando o estoque aqui
                    for produto in compras:
                        nome_produto = produto['nome']
                        quantidade_comprada = produto['quantidade']
                        
                        # Obtendo a quantidade atual do produto no estoque
                        response = requests.get(f"{server_host}produtos/{nome_produto}")
                        if response.status_code == 200:
                            produto_servidor = response.json()
                            quantidade_real = produto_servidor['quantidade']
                        
                            # Já foi verificado acima que isso é seguro
                            quantidade_real -= quantidade_comprada
                            atualizar_estoque(nome_produto, quantidade_real)
                        
                        else:
                            print(f"Erro ao atualizar o estoque do produto {nome_produto}.")
                            
                    compras = []
                else:
                    print("\nErro ao realizar compra.")

        elif escolha == '5':
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida!")

        input("\nPressione Enter para continuar...")  # Pausa para leitura
        clear_terminal()

if __name__ == "__main__":
    main()
