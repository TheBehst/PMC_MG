import serial
import time
import socket


arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)


server_ip = '192.168.2.99'
server_port = 42069
buffer_size = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("hello im here")
sock.connect((server_ip, server_port))
print("hello im here now")

data_package = []
counter = 1


try:
    while True:
        if arduino.in_waiting > 0:
            raw_data = arduino.readline()
            print(raw_data)
            if raw_data:
                data = arduino.readline().decode('utf-8').rstrip()
                #print(data)
            
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
        else:
            time.sleep(0.6)
            print('waiting for arduino')
finally:
    data = None
    message = None
    data_package = []
    response = None
    sock.close()
            
