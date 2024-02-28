import serial
import time
import socket
import queue
import threading

def connect_to_PiCar_server(input_queu):
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
def stuff():
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)
    server_ip = '192.168.2.99'
    server_port = 42069
    buffer_size = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    data_package = []
    counter = 1

    try:
        while True:

            if arduino.in_waiting > 0:
                raw_data = arduino.readline()

                if raw_data:
                    data = arduino.readline().decode('utf-8').rstrip()
                    data_package.append(data)
                    print(data_package)

                    if len(data_package) >= 10:
                        message = ','.join(data_package)
                        sock.sendall(str(message).encode('utf-8'))
                        print("Finished making package : ", counter)
                        counter += 1
                        data_package = []
                        response = sock.recv(buffer_size).decode('utf-8')
                        print(f"response from FPGA : {response}")
    finally:
        data = None
        message = None
        data_package = []
        response = None
        sock.close()
            
if __name__ == "__main__":
    input_queue = queue.Queue()
    PiCar_thread = threading.Thread(target=connect_to_PiCar_server, args=(input_queue,), daemon=True)
    PiCar_thread.start()

    data_thread