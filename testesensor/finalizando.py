# -*- coding: utf-8 -*-
import socket
import json
import threading
import mercury
import sys
from datetime import datetime

def leitor():
    param = 2300

    if len(sys.argv) > 1:
        param = int(sys.argv[1])

    # Configura a leitura na porta serial onde está o sensor
    reader = mercury.Reader("tmr:///dev/ttyUSB0")

    # Para funcionar use sempre a região "NA2" (Américas)
    reader.set_region("NA2")

    # Não altere a potência do sinal para não prejudicar a placa
    reader.set_read_plan([1], "GEN2", read_power=param)

    # Realiza a leitura das TAGs próximas
    epcs = reader.read()

    # Cria uma lista vazia para armazenar os EPCs
    epc_list = []

    # Adiciona cada tag EPC à lista
    for tag in epcs:
        epc_list.append(tag.epc)

    return epc_list

# Função para tratar cada cliente em um thread separado
def handle_client(client_socket, produtos):
    # Convertendo a lista de produtos para string JSON
    produtos_json = json.dumps(produtos)
    
    # Enviando a string JSON para o cliente
    client_socket.sendall(produtos_json.encode('utf-8'))
    print("Dados enviados para o cliente")
    
    # Fechando o socket do cliente
    client_socket.close()

def main():
    # Populando a lista de produtos
    produtos = [
        {"nome": "Maçã", "preco": 1.2, "quantidade": 10},
        {"nome": "Banana", "preco": 0.5, "quantidade": 20},
        {"nome": "Laranja", "preco": 1.0, "quantidade": 15},
        {"nome": "Pera", "preco": 1.5, "quantidade": 12}
    ]
    
    # Criando o socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Vinculando o socket a uma porta
    server_socket.bind(("172.16.103.0", 8001))
    
    # Escutando por conexões de clientes
    server_socket.listen(5)
    
    print("Servidor rodando e esperando por conexões...")
    
    while True:
        # Aceitando uma nova conexão do cliente
        client_socket, client_address = server_socket.accept()
        print("Conexão estabelecida com {client_address}")
        
        # Criando um novo thread para tratar o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, produtos))
        client_thread.start()

if __name__ == "__main__":
    main()
