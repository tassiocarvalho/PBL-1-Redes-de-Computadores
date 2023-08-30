import socket
import json
import threading

# Função para tratar cada cliente em um thread separado
def handle_client(client_socket, produtos):
    # Convertendo a lista de produtos para string JSON
    produtos_json = json.dumps(produtos)
    
    # Enviando a string JSON para o cliente
    client_socket.sendall(produtos_json.encode('utf-8'))
    print(f"Dados enviados para o cliente")
    
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
    server_socket.bind(("192.168.1.24", 8001))
    
    # Escutando por conexões de clientes
    server_socket.listen(5)
    
    print("Servidor rodando e esperando por conexões...")
    
    while True:
        # Aceitando uma nova conexão do cliente
        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}")
        
        # Criando um novo thread para tratar o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, produtos))
        client_thread.start()

if __name__ == "__main__":
    main()
