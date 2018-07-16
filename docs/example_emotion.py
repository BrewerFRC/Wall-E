from controllers import drive, head as headControl
from emotions import emotions2 as emotions
from emotions import actions
from controllers import arms as armController
#
# FUNCTIONS
#
def playSnd(file) :
	global channel
	file = "/home/pi/Wall-E/Sounds/" + file
	if file[-3:] == "wav":
		channel.play(pygame.mixer.Sound(file))
	else:
		pygame.mixer.music.load(file)
		pygame.mixer.music.play()
# Instantiates the arm system.
arms = armController.Arms();
# Head servo
head = headControl.Head()
"""
Arms Up Emotion
"""
#Arms up emotion - used as an Action in the Zombie emotion.
armsUp = emotions.Emotion(time=0)
#Create an action that runs the arms up at time zero.
armsUpAction = actions.Action(armsUpRun, time=0)
#Add the action to the ArmsUp emotion.
armsUp.addAction(armsUpAction)

"""
Zombie Emotion
"""
#Define an emotion that makes Wall-E act like a Zombie
zombie = emotions.Emotion()
#Add the arms up emotion as an action.
zombie.addAction(armsUp)
#Define an action that looks down
lookDownAction = actions.Action(lookDownRun, trigger=lookDownTrigger)
zombie.addAction(lookDownAction)


"""
Emotion Function Definitions
"""
#Define the function that runs the arms up and listens for completion.
def armsUpRun(self):
    arms.left_shoulder.moveAbs(45)
    arms.right_shoulder.moveAbs(45)
    if arms.left_shoulder.complete() and arms.right_shoulder.complete():
        self.complete = True

#Define a function that checks if the armsup action is complete.
def lookDownTrigger(self):
        return armsUp.complete()

#Define a function that moves the head down and listens for its completion.
def lookDownRun(self):
    head.lookDown()
    if head.isDown():
        playSnd("ROAR.mp3")
        self.complete = True
