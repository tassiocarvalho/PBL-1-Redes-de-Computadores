import mercury
import socket
import json
import threading
from datetime import datetime

def id_tags():
    # Dicionário de IDs RFID para produtos e preços
    rfid_products = {
        b'E2000017221101241890547C': {'name': 'Banana', 'price': 5.00},
        b'E2000017221100961890544A': {'name': 'Pacoca', 'price': 10.00},
        b'E2000017221101321890548C': {'name': 'Laranja', 'price': 12.00},
        b'E20000172211010118905454': {'name': 'Melancia', 'price': 8.00},
        b'E20000172211011718905474': {'name': 'Arroz', 'price': 15.00},
        b'E20000172211009418905449': {'name': 'Feijao', 'price': 7.00},
        b'E20000172211012518905484': {'name': 'Pera', 'price': 11.00},
        b'E20000172211011118905471': {'name': 'Macarrao', 'price': 14.00},
        b'E20000172211010218905459': {'name': 'Goiaba', 'price': 6.50},
    }
    
    param = 2300
    
    if len(sys.argv) > 1:
        param = int(sys.argv[1])

    reader = mercury.Reader("tmr:///dev/ttyUSB0")
    reader.set_region("NA2")
    reader.set_read_plan([1], "GEN2", read_power=param)
    epcs = map(lambda tag: tag, reader.read())
    tags = reader.read()
    for tag in epcs:
        print(tag.epc, tag.read_count, tag.rssi, datetime.fromtimestamp(tag.timestamp))

    
    
    produtos = []
    for tag in tags:
        product_info = rfid_products.get(tag.epc, {'name': 'Produto desconhecido', 'price': 0})
        produtos.append(product_info)
        
    return produtos

def handle_client(client_socket, produtos):
    produtos_json = json.dumps(produtos)
    client_socket.sendall(produtos_json.encode('utf-8'))
    client_socket.close()

def main():
    # Inicialmente a lista está vazia. Você pode preenchê-la usando a função id_tags()
    produtos = []
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("172.16.103.0", 5050))
    server_socket.listen(5)
    
    print("Servidor rodando e esperando por conexões...")
    
    while True:
        # Atualiza a lista de produtos com base nas tags RFID lidas
        produtos = id_tags()
        
        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}")
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket, produtos))
        client_thread.start()

if __name__ == "__main__":
    main()
