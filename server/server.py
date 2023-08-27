import socket
import json
import re

HOST, PORT = '192.168.1.24', 8000

data_store = {
    'caixa': [],
    'compras': []
}

def handle_request(data):
    headers = data.split('\r\n')
    request_line = headers[0].split()
    method, path = request_line[0], request_line[1]

    # Implementando apenas GET e POST para simplicidade
    if method == 'GET':
        if path == '/caixa':
            return 200, json.dumps(data_store['caixa'])
        elif path == '/compras':
            return 200, json.dumps(data_store['compras'])
        else:
            return 404, "Not Found"
    elif method == 'POST':
        content_length = int(re.search(r'Content-Length: (\d+)', data).group(1))
        body = data[-content_length:]
        item = json.loads(body)

        if path == '/caixa':
            data_store['caixa'].append(item)
            return 201, "Item added to caixa"
        elif path == '/compras':
            data_store['compras'].append(item)
            return 201, "Item added to compras"
        else:
            return 404, "Not Found"
    else:
        return 405, "Method Not Allowed"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                status_code, response = handle_request(data)
                conn.sendall(f"HTTP/1.1 {status_code} OK\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode('utf-8'))

if __name__ == "__main__":
    main()
