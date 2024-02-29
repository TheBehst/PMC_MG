from picar import front_wheels
from picar import back_wheels
import picar
import time


MAX_ANGLE = 45
MIN_ANGLE = -45
MAX_SPEED_FORWARD = 100
MAX_SPEED_BACKWARD = 100

sleep_time = 0.01

class Mechanics:
    def __init__(self):
        picar.setup()
        self.fw = front_wheels.Front_Wheels(db='config_picar.conf')
        self.bw = back_wheels.Back_Wheels(db='config_picar.conf')
        self.current_speed = 0
        self.current_angle = 0 # >0 : turning right, <0: turning left
        self.target_angle = 0
        self.direction = 1 # 1 = Forward, 0 = Backwards
        self.bw.forward()


    def stop_now(self):
        while (self.current_speed > 0):
            self.decelerate()
            time.sleep(sleep_time)


    def go_now(self):
        if self.direction == 1: 
            local_max_speed = MAX_SPEED_FORWARD
        else:
            local_max_speed = MAX_SPEED_BACKWARD
        while (self.current_speed != local_max_speed):
            self.accelerate()
            time.sleep(sleep_time)
    

    def turn_now(self, angle):
        self.target_angle = angle
        while  (self.current_angle != self.target_angle):
            self.turn()
            time.sleep(sleep_time)


    def talk_to_me_baby(self):
        print('HERE WE GO')
        self.turn_now(45)
        self.invert_wheels(1)
        while self.current_angle != self.target_angle:
            self.turn()
            time.sleep(sleep_time)
        self.turn_now(0)
        self.go_now()
        self.stop_now()
        self.change_direction()
        while (self.current_speed != MAX_SPEED_BACKWARD):
            self.accelerate()
            time.sleep(sleep_time)
        self.stop_now()
        self.change_direction()
        print('WAHOO')


    def accelerate(self):
        if self.direction == 1: 
            local_max_speed = MAX_SPEED_FORWARD
        else:
            local_max_speed = MAX_SPEED_BACKWARD
        if self.current_speed+1 <= local_max_speed:
            self.bw.speed = self.current_speed+1
            self.current_speed = self.current_speed+1


    def decelerate(self):
        if self.current_speed > 0:
            self.bw.speed = self.current_speed-1
            self.current_speed = self.current_speed-1


    def turn(self):
        if (self.current_angle != self.target_angle):
            if (self.current_angle < self.target_angle):
                self.current_angle += 1
            elif (self.current_angle > self.target_angle):
                self.current_angle -= 1
            self.fw.turn(self.current_angle + 90)


    def set_target_angle(self, target_angle):
        if target_angle > MAX_ANGLE:
            self.target_angle = 45
        elif target_angle < MIN_ANGLE:
            self.target_angle = -45
        else: 
            self.target_angle = target_angle


    def invert_wheels(self, inversion_coefficient):
        self.set_target_angle(-int(self.current_angle*inversion_coefficient))
    

    def change_direction(self):
        self.stop_now()
        if self.direction == 1:
            self.bw.backward()
            self.direction = 0
        else:
            self.bw.forward()
            self.direction = 1
