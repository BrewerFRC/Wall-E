import maestro
import protocol

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
    def __init__(self, maestro_channel, pot_channel):
        self.controller = maestro.Controller(channel)
        self.pot = protocol.Potentiometer(pot_channel)
