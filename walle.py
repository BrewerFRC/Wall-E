############################################
##                walle.py                ##
############################################
## A robot created by Orange Chaos (4564) ##
##                                        ##
## Authors:                               ##
##      Steven Jacobs                     ##
##      Connor Billings                   ##
##      Brent Roberts                     ##
##      Evan McCoy                        ##
##      Nate Wilcox                       ##
##                                        ##
## Published: Summer, 2014                ##
## Updated: Summer, 2017                  ##
############################################

import xbox
from controllers import controllers, drivetrain, head, arms
import pygame, random, time
import emotions

# CONSTANTS
yawSpeed = 30
pitchSpeed = 30

# BOOLEANS
slowDriveMode = False
driveDisabled = False

# Channels for Servo Controller #1
CH_LEFT_MOTOR  = 1
CH_RIGHT_MOTOR = 0
# Channels for arm vertical movement
CH_LEFT_ARM_VERT = 2
CH_RIGHT_ARM_VERT = 3
# Channels for hand servos
CH_LEFT_HAND = 4
CH_RIGHT_HAND = 5

#
# FUNCTIONS
#
def playSnd(file) :
	global channel
	file = "/home/pi/walle/Sounds/" + file
	if file[-3:] == "wav":
		channel.play(pygame.mixer.Sound(file))
	else:
		pygame.mixer.music.load(file)
		pygame.mixer.music.play()

#
# INITIALIZATION
#

# Joystick
j1 = xbox.Joystick(0)
j2 = xbox.Joystick(1)

# Emotions
emotion = emotions.Emotions(head, arms)

# Sound
pygame.mixer.init(22050, -16, 1, 1024)
channel = pygame.mixer.Channel(1)
sounds = [
        "Chatter 2.mp3",
	"Motor whir 3.mp3",
	"Jitters.mp3",
	"Motor whir 4.mp3",
	"Ohhhh.mp3",
        "Oooh.mp3",
        "Shakey shakey.mp3",
        "Whir Click.mp3",
        "Whoa 2.mp3"
]


#
# MAIN LOOP
#
print ("Wall-E RISES!!!!!!!!!!")
try:
        idleTimer = time.time()  # Timer to determine if we should switch to Idle mode
        idleWait = 0   # Timer value for next idle event occurence
        mode = "manual"
	while True :
		# Drive
		arms.update()
		if j1.connected():
                        if driveDisabled == False:
                                if slowDriveMode == True:
                                        drivetrain.drive(j1.leftX() * .4, -(j1.leftY() * .5))
                                else:
                                        drivetrain.drive(j1.leftX() * .5, -(j1.leftY()))
		else:
			drivetrain.stop()



                # Head

                # if the joystick is centered for 5 seconds, change to idle mode
                #print mode,j.rightX(),j.rightY()
                if (abs(j1.rightX()) <.1 and abs(j1.rightY()) < .1 and abs(j2.leftTrigger()) < .1 and abs(j2.rightTrigger()) < .1):
                        if j2.B() or time.time() - idleTimer >= 12:
                                mode = "idle"
                                head.stopHead()
                else:
                        mode = "manual"
                        idleTimer = time.time()

                # Interactive control
                if mode == "manual":
                        # Move head in direction of right joystick
                        head.manualMove(j1.leftX() * .5, j1.rightY())

                        # Move the brow
                        if j2.rightTrigger() > .5:
                                head.browUp()
                                idleTimer = time.time()
                        elif j2.leftTrigger() > .5:
                                head.browDown()
                                idleTimer = time.time()
                        else:
                                head.browCenter()

                        # Move head back to center position
                        if j1.whenRightThumbstick():
                                head.lookCentered()

                if mode == "idle":
                        # Is it time to start an idle move?
                        if time.time() > idleWait:
                                idleWait = time.time() + random.randint(2,10) #Next idle event wait time
                                #
                                look = random.randint(1, 17)
                                if look == 1:
                                        head.lookUp()
                                elif look == 2:
                                        head.lookDown()
                                elif look == 3:
                                        head.lookLeft()
                                elif look == 4:
                                        head.lookRight()
                                elif look >=5 and look <= 6:
                                        brow =random.randint(1,3)
                                        if brow == 1:
                                                head.browUp()
                                        if brow == 2:
                                                head.browCenter()
                                        if brow == 3:
                                                head.browDown()
                                elif look >= 7 and look <= 8:
                                        emotion.Outburst()
                                else:
                                        head.lookCentered(0.5)

                #speed Toggle and drive enable/disable
                if j.Back():
                        driveDisabled = True
                if j.Start():
                        driveDisabled = False
                if not driveDisabled:
                        if j.dpadDown():
                                slowDriveMode = True
                        if j.dpadUp():
                                slowDriveMode = False



		# Play Sounds if B button is pressed
		if j2.whenLeftBumper():
                        playSnd(sounds[random.randint(0, 8)])

		# Play "WALL-E" if Y button is pressed
		if j1.whenY() or j2.whenY():
                        idleWait = time.time() + random.randint(2,10) #Next idle event wait time
                        mode = "idle"
                        emotion.intro()

		# Print test results if A button is pressed
		if j2.whenA():
                        print(servo.isMoving(0),servo.isMoving(1))


		# Play a random emotion if X Button is pressed
		if j2.whenRightBumper():
                        idleWait = time.time() + random.randint(2,10) #Next idle event wait time
                        mode = "idle"
                        emotion.Outburst()

except:
	drivetrain.close()
	servo.close()
	j.close()
	raise
