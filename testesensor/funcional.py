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

    reader = mercury.Reader("tmr:///dev/ttyUSB0")
    reader.set_region("NA2")
    reader.set_read_plan([1], "GEN2", read_power=param)

    epcs = reader.read()
    epc_list = []
    for tag in epcs:
        epc_list.append(tag.epc)

    return epc_list

def update_products_from_tags(tag_list, tag_predefinida, produtos):
    for tag in tag_list:
        if tag in tag_predefinida:
            produtos.append(tag_predefinida[tag])

def handle_client(client_socket, produtos):
    produtos_json = json.dumps(produtos)
    client_socket.sendall(produtos_json.encode('utf-8'))
    print("Dados enviados para o cliente")
    client_socket.close()

def main():
    produtos = []
    
    tag_predefinida = {
        b'E2000017221101241890547C': {"nome": 'Banana', "preco": 5.00, 'quantidade': 1},
        b'E2000017221100961890544A': {"nome": 'Pacoca', "preco": 10.00, 'quantidade': 1},
        b'E2000017221101321890548C': {"nome": 'Laranja', "preco": 12.00, 'quantidade': 1},
        b'E20000172211010118905454': {"nome": 'Melancia', "preco": 8.00, 'quantidade': 1},
        b'E20000172211011718905474': {"nome": 'Arroz', "preco": 15.00, 'quantidade': 1},
        b'E20000172211009418905449': {"nome": 'Feijao', "preco": 7.00, 'quantidade': 1},
        b'E20000172211012518905484': {"nome": 'Pera', "preco": 11.00, 'quantidade': 10},
        b'E20000172211011118905471': {"nome": 'Macarrao', "preco": 14.00, 'quantidade': 10},
        b'E20000172211010218905459': {"nome": 'Goiaba', "preco": 6.50, 'quantidade': 10},
    }
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("172.16.103.0", 8001))
    server_socket.listen(5)
    
    print("Servidor rodando e esperando por conexões...")
    
    while True:
        produtos = []  # Limpa a lista de produtos para cada ciclo
        tag_list = leitor()
        update_products_from_tags(tag_list, tag_predefinida, produtos)

        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}")
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket, produtos))
        client_thread.start()

if __name__ == "__main__":
    main()
