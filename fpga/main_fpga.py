import socket

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"Server started at {ip}:{port}")
    return server_socket

def handle_client_connection(client_socket):
    buffer_size = 1024
    try:
        while True:
            data = client_socket.recv(buffer_size)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received: {message}")
            # Send a response back to the client
            response = "ACK"
            client_socket.sendall(response.encode('utf-8'))
    finally:
        client_socket.close()

def main():
    ip = '192.168.2.99'
    port = 42069
    server_socket = start_server(ip, port)
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            handle_client_connection(client_socket)
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()