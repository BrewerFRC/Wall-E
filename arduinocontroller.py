
class Arduino:

    def __init__(self,port=1):
        ttyStr = '/dev/ttyACM' + str(port)
        self.usb = serial.Serial(ttyStr)

    def sendCommand(self, command):
        usb.write(command.encode())

    def getServoMotor(self, channel):
        return _ServoMotor(channel, self)


class _ServoMotor:

    def __init__(self, channel, arduino):
        self.channel = channel
        self.arduino = arduino

    # Set minimum allowed position from -1.0 to 1.0
    def setMin(min):
        self.min = (min + 1) * 90
        self.arduino.sendCommand('m' + chr(channel) + chr(min))

    # Set maximum allowed position from -1.0 to 1.0
    def setMax(max):
        self.max = (max + 1) * 90
        self.arduino.sendCommand('M' + chr(channel) + chr(max))

    # Set the target position from -1.0 to 1.0
    def setTarget(target):
        self.target = (target + 1) * 90
        self.arduino.sendCommand('T' + chr(channel) + chr(target))

    # Set the target speed of movement from 0 to 1 (1 = 1 second between extremes)
    def setTargetSpeed(speed):
        self.speed = int((speed + 1) / 2 * 255)
        self.arduino.sendCommand('S' + chr(channel) + chr(target))

    # Set the acceleration of the motors when approaching target speed, -1 to 1
    def setAcceleration(acceleration):
        self.acceleration = int((acceleration + 1) / 2 * 255))
        self.arduino.sendCommand('A' + chr(channel) + chr(target))

    def getPosition(self):
        pass
