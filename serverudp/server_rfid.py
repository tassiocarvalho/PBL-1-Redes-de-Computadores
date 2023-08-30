import socket
import json
import threading

# Função para tratar cada cliente em um thread separado
def handle_client(client_address, server_socket, produtos):
    # Convertendo a lista de produtos para string JSON
    produtos_json = json.dumps(produtos)
    
    # Enviando a string JSON para o cliente
    server_socket.sendto(produtos_json.encode('utf-8'), client_address)
    print(f"Dados enviados para {client_address}")

def main():
    # Populando a lista de produtos
    produtos = [
        {"nome": "Maçã", "preco": 1.2, "quantidade": 10},
        {"nome": "Banana", "preco": 0.5, "quantidade": 20},
        {"nome": "Laranja", "preco": 1.0, "quantidade": 15},
        {"nome": "Pera", "preco": 1.5, "quantidade": 12}
    ]
    
    # Criando o socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Vinculando o socket a uma porta
    server_socket.bind(("192.168.1.24", 8000))
    
    print("Servidor rodando e esperando por mensagens...")
    
    while True:
        # Recebendo dados do cliente
        data, client_address = server_socket.recvfrom(1024)
        
        # Criando um novo thread para tratar o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_address, server_socket, produtos))
        client_thread.start()

if __name__ == "__main__":
    main()
