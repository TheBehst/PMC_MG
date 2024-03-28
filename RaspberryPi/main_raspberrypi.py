import serial
import time
import socket
import queue
import threading
import matplotlib.pyplot as plt 
import numpy as np
from traitement import *

def connect_to_PiCar_server(input_queu):
    host = '192.168.43.203'  # Replace SERVER_IP with the server's IP address
    port = 12345     # Port number must match the server's port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            #TODO changer pour prendre les valeurs du fpga
            value = input("give input : ")
            s.sendall(value.encode())
            data = s.recv(1024)
            print(f"Received: {data.decode()}")
            if data.decode() == "server byebye":
                print("server said byebye")
                break
            
def connect_Arduino_to_FPGA(input_queue):
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)
    server_ip = '192.168.2.99'
    server_port = 42069
    buffer_size = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    counter = 1

    try:
        while True:

            if arduino.in_waiting > 0:
                raw_data = arduino.readline()

                if raw_data:
                    emg_data = int(arduino.readline().decode('utf-8').rstrip())
                    data_package = detect_and_format_activity(emg_data, threshold=80)
                    #data_package.append(data)
                    print(data_package)

                    if data_package is not None:
                        message = ','.join(map(str, data_package))
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

def connect_Arduino_to_FPGAtest(input_queue):
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)
    # server_ip = '192.168.2.99'
    # server_port = 42069
    # buffer_size = 1024
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((server_ip, server_port))
    counter = 1
    t = np.arange(0, 100)

    try:
        while True:

            if arduino.in_waiting > 0:
                raw_data = arduino.readline()

                if raw_data:
                    emg_data = int(arduino.readline().decode('utf-8').rstrip())
                    print(emg_data)
                    data_package = detect_and_format_activity(emg_data, threshold=350)
                    #data_package.append(data)
                    # print(data_package)

                    if data_package is not None:
                        with open(f"PMC_MG/RaspberryPi/SpikeData/testData{counter}.txt", "w") as file:
                            for item in data_package:
                                file.write(f"{item}")
                        counter += 1

                        plt.figure()
                        plt.plot(t, data_package)
                        plt.xlabel("time")
                        plt.ylabel("EMG value")
                        plt.grid(True)
                        plt.show()
                        
    finally:
        data = None
        message = None
        data_package = []
        response = None
        # sock.close()
            
if __name__ == "__main__":

    input_queue = queue.Queue()
    fpga_thread = threading.Thread(target=connect_Arduino_to_FPGAtest(input_queue), args=(input_queue,), daemon=True)
    fpga_thread.start()

    # connect_to_PiCar_server(input_queue)