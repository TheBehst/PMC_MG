import socket

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