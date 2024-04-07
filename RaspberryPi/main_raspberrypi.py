import serial
import time
import socket
import queue
import threading
import matplotlib.pyplot as plt 
import numpy as np
from traitement import *
DEVICE = "PC"
FENETRAGE = False
baud_rate = 19200
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

def connect_to_Arduino():
    if DEVICE == "PI":
        connection = serial.Serial('/dev/ttyUSB0', baud_rate)
        time.sleep(2)
    elif DEVICE == "PC":
        serial_port = 'COM5'
        connection = serial.Serial(serial_port, baud_rate)
        time.sleep(2)

    return connection

def connect_Arduino_to_FPGAtest(input_queue):
    arduino_connection = connect_to_Arduino()
    counter = 1
    t = np.arange(0, 100)
    preprocessor = Preprocess(threshold = 15)

    try:
        while True:

            if arduino_connection.in_waiting > 0:
                raw_data = arduino_connection.readline()

                if raw_data:
                    emg_data = int(arduino_connection.readline().decode('utf-8').rstrip())
                    print(f"data from arduino : {emg_data}")

                    if FENETRAGE:
                        preprocessor.detect_format_activity(emg_data)
                        data_package = preprocessor.formatted_data

                        if data_package is not None:
                            with open(f"RaspberryPi/Data/testData{counter}.txt", "w") as file:
                                for item in data_package:
                                    file.write(f"{item}\n")
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
        arduino_connection.close()
        # sock.close()

def connect_Arduino_to_FPGAtestread(input_queue):
    arduino = serial.Serial('/dev/ttyUSB0', 19200)
    time.sleep(2)
    # server_ip = '192.168.2.99'
    # server_port = 42069
    # buffer_size = 1024
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((server_ip, server_port))
    counter = 1
    t = np.arange(0, 100)
    preprocessor = Preprocess(threshold = 15)
    try:
        while True:

            if arduino.in_waiting > 0:
                raw_data = arduino.readline()

                if raw_data:
                    emg_data = int(arduino.readline().decode('utf-8').rstrip())
                    print(f"data from arduino : {emg_data}")
                    #preprocessor.detect_format_activity(emg_data)
                    #data_package = preprocessor.formatted_data

    finally:
        data = None
        message = None
        data_package = []
        response = None
        # sock.close()
def connect_Arduino_to_FPGAtestpres(input_queue):
    # arduino = serial.Serial('/dev/ttyUSB0', 9600)
    # time.sleep(2)
    # server_ip = '192.168.2.99'
    # server_port = 42069
    # buffer_size = 1024
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((server_ip, server_port))
    counter = 1
    t = np.arange(0, 1000, 10)
    with open('Data/test.txt', 'r') as file:
        # Read the file's contents and split into a list, one element per line
        data_list = file.read().splitlines()

    preprocessor = Preprocess(threshold = 15)
    try:
        #while True:

        # if arduino.in_waiting > 0:
        #     raw_data = arduino.readline()
        plt.figure()
        t_list = [10*e for e in [np.arange(0, len(data_list))]]
        data_list = [int(element) for element in data_list]
        #print(data_list)
        plt.plot(t_list[0], data_list)
        plt.xlabel("time(ms)")
        plt.ylabel("EMG value")
        plt.grid(True)
        plt.title("Original data")
        plt.show()
        for data in data_list:
            # emg_data = int(arduino.readline().decode('utf-8').rstrip())
            # print(emg_data)
            preprocessor.detect_format_activity(data)
            data_package = preprocessor.formatted_data
            #data_package.append(data)
            # print(data_package)
            
            if data_package is not None:
                with open(f"Data/saveData{counter}.txt", "w") as file:
                    for item in data_package:
                        file.write(f"{item}\n")
                plt.figure()
                plt.plot(t, data_package)
                plt.xlabel("time(ms)")
                plt.ylabel("EMG value")
                plt.title("Spike data")
                plt.grid(True)
                plt.show()
                counter += 1
                preprocessor.formatted_data = None
                        
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