import serial
import time
import socket
import queue
import threading
from mechanics import Mechanics

def connect_to_PiCar_server(input_queue):
    host = '192.168.43.203'  # Replace SERVER_IP with the server's IP address
    port = 12345     # Port number must match the server's port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            #TODO changer pour prendre les valeurs du fpga
            value =  input_queue.get()
            s.sendall(value.encode())
            data = s.recv(1024)
            print(f"Received: {data.decode()}")
            if data.decode() == "server byebye":
                print("server said byebye")
                break
def stuff(input_queue):
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)
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
                        command = False
                        for dat in data_package:
                            if dat > 1000:
                                command = True
                        if command: 
                            input_queue.put('w')
                            print("spike detected!")
                            
                        data_package = []

    finally:
        data = None
        message = None
        data_package = []

def main():
    print("BEGIN")
    while True:
        print("big while")
        mechanics = Mechanics()
        mechanics.stop_now()

        input_queue = queue.Queue()
        lecture_thread = threading.Thread(target=stuff, args=(input_queue,), daemon=True)
        lecture_thread.start()
        
        connect_to_PiCar_server(input_queue)
        lecture_thread.join()
    print("END")


if __name__ == "__main__":
    main()
