import socket

class InternetSocket:
    def __init__(self) -> None:
        pass

    def create_server(host, port):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.bind((host, port))
        my_socket.listen()
        
        print("server started")
        return my_socket


    def connect_to_server(ip, port):
        host = ip   # Replace SERVER_IP with the server's IP address

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            while True:
                value = input("give input : ")
                s.sendall(value.encode())
                data = s.recv(1024)
                print(f"Received: {data.decode()}")
                if data.decode() == "server byebye":
                    print("server said byebye")
                    break