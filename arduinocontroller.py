import time
import serial

TIMEOUT = 0.001

class Arduino:

    def __init__(self,port=1):
        ttyStr = '/dev/ttyACM' + str(port)
        self.usb = serial.Serial(ttyStr)

    def sendCommand(self, command):
        usb.write(command.encode())

    def getServoMotor(self, channel):
        return _ServoMotor(channel, self)

    def _read(self):
        timeout = time.time() + TIMEOUT
        while(time.time() < timeout):
            command = str(self.usb.read(self.usb.in_waiting))
        return command

    def getCommand(self):
        command = self._read()
        action = command[:1]
        channel = int(command[1:2])
        value = 0
        if len(command) >= 3:
            value = int(command[2:])
        return action, channel, value

class _ServoMotor:

    def __init__(self, channel, arduino):
        self.channel = channel
        self.arduino = arduino

    # Set minimum allowed position from -1.0 to 1.0
    def setMin(min):
        self.min = (min + 1) * 90
        self.arduino.sendCommand('m' + chr(channel + 48) + str(min))

    # Set maximum allowed position from -1.0 to 1.0
    def setMax(max):
        self.max = (max + 1) * 90
        self.arduino.sendCommand('M' + chr(channel + 48) + str(max))

    # Set the target position from -1.0 to 1.0
    def setTarget(target):
        self.target = (target + 1) * 90
        self.arduino.sendCommand('T' + chr(channel + 48) + str(target))

    # Set the target speed of movement from 0 to 1 (1 = 1 second between extremes)
    def setTargetSpeed(speed):
        self.speed = int((speed + 1) / 2 * 255)
        self.arduino.sendCommand('S' + chr(channel + 48) + str(target))

    # Set the acceleration of the motors when approaching target speed, -1 to 1
    def setAcceleration(acceleration):
        self.acceleration = int((acceleration + 1) / 2 * 255))
        self.arduino.sendCommand('A' + chr(channel + 48) + str(target))

    def getPosition(self):
        self.arduino.sendCommand('P' + chr(channel + 48))
        action, channel, value = self.arduino.getCommand()
        if self.channel == channel and action == 'P':
            return value
