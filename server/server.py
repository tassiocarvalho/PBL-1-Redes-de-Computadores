import socket
import json
import re
import threading
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

#HOST, PORT = '192.168.1.24', 8000
from ipconfig import hostip, server_host, port

data_store = {
    'caixa': [{"id": 666,"status": True}],
    'compras': [],
    'produtos': [
    {"nome": "Banana", "preco": 5.00, "quantidade": 100},
    {"nome": "Pacoca", "preco": 10.00, "quantidade": 100},
    {"nome": "Laranja", "preco": 12.00, "quantidade": 100},
    {"nome": "Melancia", "preco": 8.00, "quantidade": 100},
    {"nome": "Arroz", "preco": 15.00, "quantidade": 100},
    {"nome": "Feijao", "preco": 7.00, "quantidade": 100},
    {"nome": "Pera", "preco": 11.00, "quantidade": 100},
    {"nome": "Macarrao", "preco": 14.00, "quantidade": 100},
    {"nome": "Goiaba", "preco": 6.50, "quantidade": 100}
]
}

def handle_request(data):
    headers = data.split('\r\n')
    request_line = headers[0].split()
    method, path = request_line[0], request_line[1]

    # Implementando apenas GET e POST para simplicidade
    if method == 'GET':
        if path == '/caixa':
            return 200, json.dumps(data_store['caixa'])
        elif re.match(r'/caixa/\d+', path):
            caixa_id = int(path.split('/')[-1])
            caixa = next((item for item in data_store['caixa'] if item['id'] == caixa_id), None)
            if caixa:
                return 200, json.dumps(caixa)
            else:
                return 404, json.dumps({"mensagem": "Caixa não encontrado"})
        elif re.match(r'/produtos/[^/]+', path):
            product_name = path.split('/')[-1]
            product = next((item for item in data_store['produtos'] if item['nome'] == product_name), None)
            if product:
                return 200, json.dumps(product)
            else:
                return 404, json.dumps({"mensagem": "Produto não encontrado"})
        elif path == '/compras':
            return 200, json.dumps(data_store['compras'])
        elif path == '/produtos':  # Aqui está a nova rota para produtos
            return 200, json.dumps(data_store['produtos'])
        else:
            return 404, json.dumps({"mensagem": "Não encontrado"})
    elif method == 'POST':
        content_length = int(re.search(r'Content-Length: (\d+)', data).group(1))
        body = data[-content_length:]
        item = json.loads(body)

        if path == '/caixa':
            existing_caixa = next((caixa for caixa in data_store['caixa'] if caixa['id'] == item['id']), None)
            if existing_caixa:
                return 409, json.dumps({"mensagem": "Caixa com o mesmo ID já existe"})
            else:
                data_store['caixa'].append(item)
                return 201, json.dumps({"mensagem": "Item adicionado ao caixa"})
        elif path == '/compras':
            data_store['compras'].append(item)
            return 201, json.dumps({"mensagem": "Item adicionado às compras"})
        elif path == '/produtos':  # Nova condição para adicionar produtos
            existing_product = next((product for product in data_store['produtos'] if product['nome'] == item['nome']), None)
            if existing_product:
                return 409, json.dumps({"mensagem": "Produto com o mesmo nome já existe"})
            else:
                data_store['produtos'].append(item)
                return 201, json.dumps({"mensagem": "Produto adicionado com sucesso"})
        else:
            return 404, json.dumps({"mensagem": "Não encontrado"})
    elif method == 'PUT':
        if re.match(r'/caixa/\d+', path):
            caixa_id = int(path.split('/')[-1])
            content_length = int(re.search(r'Content-Length: (\d+)', data).group(1))
            body = data[-content_length:]
            update_data = json.loads(body)

            caixa = next((item for item in data_store['caixa'] if item['id'] == caixa_id), None)

            if caixa:
                caixa['status'] = update_data.get('status', caixa['status'])
                return 200, json.dumps({"mensagem": "Caixa atualizado com sucesso"})
            else:
                return 404, json.dumps({"mensagem": "Caixa não encontrado"})
        elif re.match(r'/produtos/[^/]+', path):  # Regex para casar com qualquer nome de produto
            product_name = path.split('/')[-1]
            content_length = int(re.search(r'Content-Length: (\d+)', data).group(1))
            body = data[-content_length:]
            update_data = json.loads(body)
            
            # Buscando o produto pelo nome
            product = next((item for item in data_store['produtos'] if item['nome'] == product_name), None)
            
            if product:
                new_quantity = update_data.get('quantidade', product['quantidade'])
                product['quantidade'] = new_quantity  # Atualizando a quantidade
                
                return 200, json.dumps({"mensagem": f"Quantidade de {product_name} atualizada para {new_quantity}"})
            else:
                return 404, json.dumps({"mensagem": "Produto não encontrado"})
        else:
            return 404, json.dumps({"mensagem": "Não encontrado"})
    else:
        return 405, json.dumps({"mensagem": "Método não permitido"})

def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:  # Verifique se há dados antes de processá-los
            status_code, response = handle_request(data)
            conn.sendall(f"HTTP/1.1 {status_code} OK\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode('utf-8'))
    except Exception as e:
        print(f"Erro ao processar a requisição de {addr}: {e}")
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((hostip, port))
        s.listen()
        print(f"Server listening on {hostip}:{port}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()