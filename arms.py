import maestro
import protocol

#Potentiometer limits for the different joints, lowest first
RIGHT_SHOULDER_LIMITS = [0, 0]
LEFT_SHOULDER_LIMITS = [0, 0]
RIGHT_ELBOW_LIMITS = [0, 0]
LEFT_ELBOW_LIMITS = [0, 0]

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
    def __init__(self, maestro_channel, pot_channel=None, limits=None):
        self.controller = maestro.Controller(channel)
        if not pot_channel == None:
            self.pot = protocol.Potentiometer(pot_channel)
        self.limits = limits

    def moveable(self):
        if self.limits == None:
            return True
        if self.pot == None:
            return False

        position = self.pot.read()
        if position <= self.limits[1] and position >= self.limits[0]:
            return True
        return False
