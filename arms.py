import arduinocontroller
import protocol
import pid

arduino = arduinocontroller.Arduino()

#Potentiometer limits for the different joints, lowest first
RIGHT_SHOULDER_LIMITS = [0, 0]
LEFT_SHOULDER_LIMITS = [0, 0]
RIGHT_ELBOW_LIMITS = [0, 0]
LEFT_ELBOW_LIMITS = [0, 0]
MAX_SPEED = 60
MIN_SPEED = 1
ACCELERATION = 1
TOLERANCE = 0 #TODO: find allowable error

class Arms:
    def __init__(self, ch_left_shoulder=0, ch_right_shoulder=1, ch_left_elbow=2, ch_right_elbow=3, ch_left_hand=4, ch_right_hand=5, maestro):
        self.maestro = maestro
        self.left_shoulder = Joint(ch_left_shoulder)
        self.right_shoulder = Joint(ch_right_shoulder)
        self.left_elbow = Joint(ch_left_elbow)
        self.right_elbow = Joint(ch_right_elbow)
        self.left_hand = Joint(ch_left_hand, maestro=True)
        self.right_hand = Joint(ch_right_hand, maestro=True)

class Joint:
    # Limits: [upper, lower]
    def __init__(self, channel, limits=[0, 180], maestro=False):
        if maestro:
            self.controller = self.maestro.Channel(channel)
        else:
            self.controller = arduino.getServoMotor(channel)
        if limits:
            self.controller.setMin(limits[0])
            self.controller.setMax(limits[1])

    def moveable(self):
        if self.limits == None:
            return True

        position = self.controller.getPosition()
        if position <= self.limits[1] and position >= self.limits[0]:
            return True
        return False

    # Move joint (motor or servo) to specfic position along its range of motion
    # Position: 0 through 1, Speed: 0 through 1
    def move_abs(self, position, speed = 0):
        self.controller.setTargetSpeed(speed)
        self.controller.setTarget(position)

    # Returns whether or not the motor has reached its target location.
    def moving(self):
        if abs(self.controller.getPosition() - self.controller.target) < TOLERANCE:
            return True
        return False

    def complete(self):
        return not self.moving()
