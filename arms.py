import serial
import head
import time
import emotions, maestro
import random

com = serial.Serial('/dev/ttyUSB0', 115200) #Initializes serial protocal.

class Arms:
    def __init__(self, head, emotions, maestro):
        self.head = head
        self.emotions = emotions
        self.maestro = maestro
        self.timerL = 0
        self.timerR = 0
        self.wavingL = 0  #0=stopped,1=rotating
        self.wavingR = 0
    def armPos(self, channel, pos):
        if pos < 0: #Error-proofing restricts values to within 0-40 degrees, where physical range is 0-45; reduces risk of motor directional flip.
            pos = 0
        elif pos > 40:
            pos = 40
        com.write(bytearray([255, channel, pos])) #Sends command over serial with identification character 255 for arm motor-servos.


    def wristPos(self, channel, pos):
        if channel == 'l': #Sends command over serial with identification character 254 for wrist servos.
            self.maestro.setTarget(5, pos)
        else:
            self.maestro.setTarget(6, pos)


    def wave(self, arm):
        if arm == 'l':
            if self.wavingL == 0 and time.time() > self.timerL:
                self.timerL = time.time() + 0.5
                self.wavingL = 1

        elif arm == 'r':
            if self.wavingR == 0 and time.time() > self.timerR:
                self.timerR = time.time() + 0.5
                self.wavingR = 1


    def update(self):
        if self.wavingL==1:
            if time.time() < self.timerL:
                self.wristPos('l', 8200)
            else:
                self.wavingL=0
                self.timerL = time.time() + 0.5
                self.wristPos('l', 4400)

        if self.wavingR==1:
            if time.time() < self.timerR:
                self.wristPos('r', 7000)  #was 9000
            else:
                self.wavingR=0
                self.timerR = time.time() + 0.5
                self.wristPos('r', 4000)  #was 7000

