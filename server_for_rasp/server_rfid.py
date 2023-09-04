# -*- coding: utf-8 -*-
import socket
import json
import threading

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
    {"nome": "Banana", "preco": 5.00, "quantidade": 1},
    {"nome": "Pacoca", "preco": 10.00, "quantidade": 1},
    {"nome": "Laranja", "preco": 12.00, "quantidade": 1},
    {"nome": "Melancia", "preco": 8.00, "quantidade": 1},
    {"nome": "Arroz", "preco": 15.00, "quantidade": 1},
    {"nome": "Feijao", "preco": 7.00, "quantidade": 1},
    {"nome": "Pera", "preco": 11.00, "quantidade": 1},
    {"nome": "Macarrao", "preco": 14.00, "quantidade": 1},
    {"nome": "Goiaba", "preco": 6.50, "quantidade": 1}
]
    
    # Criando o socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Vinculando o socket a uma porta
    server_socket.bind(("192.168.1.24", 8001))
    
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
