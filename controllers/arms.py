from controllers import controllers
import protocol
import sys

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
    def __init__(self, ch_left_shoulder=0, ch_right_shoulder=1, ch_left_hand=2, ch_right_hand=3):
        self.left_shoulder = Joint(ch_left_shoulder, limits=[0, 45])
        self.right_shoulder = Joint(ch_right_shoulder, limits=[0, 45])
        self.left_hand = Joint(ch_left_hand, maestro=True)
        self.right_hand = Joint(ch_right_hand, maestro=True)

class Joint:
    # Limits: [upper, lower]
    def __init__(self, channel, limits=[-sys.maxint, sys.maxint], maestro=False):
        if maestro:
            self.controller = controllers.maestro.Channel(channel)
        else:
            self.controller = controllers.arduino.getMotor(channel)
        if limits:
            self.limits = limits
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
    def movePos(self, position, speed = 0):
        self.controller.setTargetSpeed(speed)
        self.controller.setTarget(position)

    # Returns whether or not the motor has reached its target location.
    def moving(self):
        if abs(self.controller.getPosition() - self.controller.target) < TOLERANCE:
            return True
        return False

    def complete(self):
        return not self.moving()
