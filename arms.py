import maestro
import protocol
import pid

#Potentiometer limits for the different joints, lowest first
RIGHT_SHOULDER_LIMITS = [0, 0]
LEFT_SHOULDER_LIMITS = [0, 0]
RIGHT_ELBOW_LIMITS = [0, 0]
LEFT_ELBOW_LIMITS = [0, 0]
MAX_SPEED = 60
MIN_SPEED = 1
ACCELERATION = 1

class Arms:
    # Shoulder: (Maestro channel, analog channel) | Hand: Maestro channel | Elbow: (Maestro channel, analog channel)
    def __init__(self, ch_left_shoulder=(2,0), ch_right_shoulder=(3,0), ch_left_elbow=(0,2), ch_right_elbow=(1,3), ch_left_hand=4, ch_right_hand=5):
        self.left_shoulder = Joint(ch_left_shoulder[0], ch_left_shoulder[1])
        self.right_shoulder = Joint(ch_right_shoulder[0], ch_right_shoulder[1])
        self.left_elbow = Joint(ch_left_elbow[0], ch_left_elbow[1])
        self.right_elbow = Joint(ch_right_elbow[0], ch_right_elbow[1])
        self.left_hand = maestro.Controller(ch_left_hand)
        self.right_hand = maestro.Controller(ch_right_hand)

class Joint:
    # Limits: [upper, lower], Targets: [backward, stop, forward], pidTerms: [P, I, D, [min, max]]
    def __init__(self, maestro_channel, pot_channel=None, limits=None, targets=[4000, 6000, 8000], servo=False, pidTerms=[0, 0, 0, [-1, 1]]):
        self.controller = maestro.Controller(channel)
        if not pot_channel == None:
            self.pot = protocol.Potentiometer(pot_channel)
        self.limits = limits
        if servo:
            self.positions = targets
        else:
            self.speeds = targets
            self.pid = pid.Pid(pidTerms[0], pidTerms[1], pidTerms[2], pidTerms[3][0], pidTerms[3][1])
        self.servo = servo

    def moveable(self):
        if self.limits == None:
            return True
        if self.pot == None:
            return False

        position = self.pot.read()
        if position <= self.limits[1] and position >= self.limits[0]:
            return True
        return False

    #speed scaling from 0 through 1, -1 is unrestricted
    #position scaling through -1 through 1
    def _move_controller(self, target, speed = -1):
        if self.moveable() == True:
            #speed of -1 is unrestricted
            if speed == -1:
                speed = 0
            else:
                speed = abs((MAX_SPEED - MIN_SPEED) * speed) + MIN_SPEED

            if position >= 0:
                target = abs((self.targets[2] - self.targets[1]) * target) + self.targets[1]
            else:
                target = abs((self.targets[1] - self.targets[0]) * target) + self.targets[0]

    def move_abs(self, position, speed = 0):
        if self.servo:
            if speed == 0:
                speed = -1
            self._move_controller(position, speed)
        else:
            self.pid.target = abs((self.limits[1] - self.limits[0]) * position) + self.limits[0]
            #TODO: PID control for completion

    def update(self):
        self._move_controller(pid.calc(self.pot.read()), ACCELERATION)
