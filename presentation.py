import serial
import time
import socket
import queue
import threading

def connect_to_PiCar_server(input_queue):
    host = '192.168.86.243'  # Replace SERVER_IP with the server's IP address
    port = 12345     # Port number must match the server's port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("connected!")
        while True:
            #TODO changer pour prendre les valeurs du fpga
            if input_queue.qsize() >= 1:
                print("something in Q")
                value =  input_queue.get()
                print(f"sending {value}")
                s.sendall(value.encode())
                
                data = s.recv(1024)
                print(f"Received: {data.decode()}")
                time.sleep(4)
                if data.decode() == "server byebye":
                    print("server said byebye")
                    break

def stuff(input_queue):
    arduino = serial.Serial('/dev/ttyUSB0', 19200)
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
                    
                    if len(data_package) >= 20:
                        print("PACKAGE: ")
                        print(data_package)
                        command = False
                        for dat in data_package:
                            if int(dat) > 1000:
                                command = True
                        if command: 
                            input_queue.put('w')
                            print("spike detected!")
                            time.sleep(1)
                            
                        data_package = []
                        

    finally:
        data = None
        message = None
        data_package = []

def main():
    print("BEGIN")
    while True:
        print("big while")

        input_queue = queue.Queue()
        lecture_thread = threading.Thread(target=stuff, args=(input_queue,), daemon=True)
        lecture_thread.start()
        
        connect_to_PiCar_server(input_queue)
        lecture_thread.join()
    print("END")


if __name__ == "__main__":
    main()
