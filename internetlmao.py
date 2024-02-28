import socket

def connect_to_server():
    host = '192.168.43.203'  # Replace SERVER_IP with the server's IP address
    port = 12345     # Port number must match the server's port

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
            
if __name__ == "__main__":
    connect_to_server()