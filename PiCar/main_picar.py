import threading
import queue
import time
import socket
import serial
from PiCar.mechanics import Mechanics
from ..internet import InternetSocket

def start_PiCar_server(input_queue):
    host = '0.0.0.0'
    port = 12345
    try:
        s = InternetSocket.create_server(host, port)
        
        
        conn, addr = s.accept()
        print("client connected")
        data = ('lmao').encode()
        with conn:
            print ('Got connection from', addr)
            while data.decode() != 'q':
                data = conn.recv(1024)
                print(f"received: {data.decode()}")
                input_queue.put(data.decode())
                conn.sendall(data)
                time.sleep(0.1)
            print("server byebye")
            conn.sendall(("server byebye").encode())
                
    except Exception as e:
        print(e)
        print("closing socket")
        s.close()
    
    finally:
        s.close()
    input_queue.put('q')
                

def control_PiCar(input_queue, mechanics):
    quit = False
    while not quit:
        if input_queue.qsize() == 1:
            input_str = input_queue.get()
            
            if input_str == 'a':
                print("left")
                mechanics.turn_now(mechanics.current_angle-45)

            elif input_str == 'd':
                print("right")
                mechanics.turn_now(mechanics.current_angle+45)
            
            elif input_str == 'w':
                print("forward")
                if mechanics.direction == 1 :
                    mechanics.go_now()
                elif mechanics.current_speed != 0:
                    mechanics.stop_now()
                else:
                    mechanics.change_direction()
                    mechanics.go_now()

            elif input_str == 's':
                print("backward")
                if mechanics.direction == 0:
                    mechanics.go_now()
                elif mechanics.current_speed != 0:
                    mechanics.stop_now()
                else:
                    mechanics.change_direction()
                    mechanics.go_now()

            elif input_str == 'q':
                print("quit")
                quit = True
            
            time.sleep(0.1)
            
def main():
    print("BEGIN")
    while True:
        print("big while")
        mechanics = Mechanics()
        mechanics.stop_now()

        input_queue = queue.Queue()
        PiCar_thread = threading.Thread(target=start_PiCar_server, args=(input_queue,), daemon=True)
        PiCar_thread.start()
        
        control_PiCar(input_queue, mechanics)
        PiCar_thread.join()
    print("END")


if __name__ == "__main__":
    main()
