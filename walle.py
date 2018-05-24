import xbox
import maestro
import pygame
import random
import drive
import head
import time
import emotions

# CONSTANTS

# BOOLEANS
Disable = False
buttonPressed = False


# Channels for Servo Controller #1
CH_LEFT_MOTOR  = 1
CH_RIGHT_MOTOR = 0


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

#
# INITIALIZATION
#

# Joystick
#j1 = xbox.Joystick(0)
#j2 = xbox.Joystick(1)
j = xbox.Joystick(0)
time.sleep(3)
# Maestro Controllers
servo = maestro.Controller()
# DriveTrain
drivetrain = drive.DriveTrain(servo,CH_RIGHT_MOTOR,CH_LEFT_MOTOR)
speedtoggle = True # false = slow, true = normal
# Head servo
head = head.Head(servo)
# Emotions
emotion = emotions.Emotions(head)
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
connected = False
try:
        idleTimer = time.time()  # Timer to determine if we should switch to Idle mode
        idleWait = 0   # Timer value for next idle event occurence
        mode = "manual"
	while True :
                #print j.connected()
		# Drive
		if j.connected():
                        if connected == False:
                                print "Joystick connected"
                                connected = True
                        if Disable == False:
                                if speedtoggle == True:
                                        drivetrain.drive(j.leftX() * .5, -(j.leftY()))
                                else:
                                        drivetrain.drive(j.leftX() * .40, -(j.leftY() * .5))
                                
		else:
			drivetrain.stop()
			if connected == True:
                                print "Joystick disconnected ",j.connected()
			connected = False
                                
                        
                # Head
                
                # if the joystick is centered for 5 seconds, change to idle mode
                #print mode,j.rightX(),j.rightY()
                if abs(j.rightX()) <.1 and abs(j.rightY()) < .1 and abs(j.leftTrigger()) < .1 and abs(j.rightTrigger()) < .1 and abs(j.leftX()) <.1 and abs(j.leftY()) < .1:
                        if time.time() - idleTimer >= 12:
                                mode = "idle"
                else:
                        mode = "manual"
                        idleTimer = time.time()
                # Interactive control
                if mode == "manual":
                        head.moveAbs(j.rightX() or j.leftX() * .5, -j.rightY())
                        if j.rightTrigger() > .5:
                                head.browUp()
                                idleTimer = time.time()
                        elif j.leftTrigger() > .5:
                                head.browDown()
                                idleTimer = time.time()
                        else:
                                head.browCenter()
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
                #speed Toggle
                if j.Back():
                        speedtoggle = False
                if j.Start():
                        speedtoggle = True

                #Drive Disable
                if j.dpadUp():
                        if j.leftBumper():
                                        if j.rightBumper():
                                                Disable = False
                                                print "Drive On"
                if j.dpadDown():
                        if j.leftBumper():
                                        if j.rightBumper():
                                                Disable = False
                                                print "Disabled"
                        
		# Play Sounds if B button is pressed
		if j.B() or j.dpadUp():
                        if j.leftBumper() or j.dpadUp():
                                if j.rightBumper() or j.dpadUp:
                                        print "whistle while you work"
                                        emotion.easterEgg(3)
                                else:
                                        playSnd(sounds[random.randint(0, 8)])
                        else:
                                playSnd(sounds[random.randint(0, 8)])
			
		# Play "WALL-E" if Y button is pressed
		if j.Y():
                        idleWait = time.time() + random.randint(2,10) #Next idle event wait time
                        mode = "idle"      
                        if j.leftBumper():
                                if j.rightBumper():
                                        emotion.easterEgg(1)
                                        print ""
                                else:
                                        emotion.intro()
                        else:
                                emotion.intro()
                                
		# Print test results if A button is pressed
		if j.A():
                        if j.leftBumper():
                                if j.rightBumper():
                                        #emotion.easterEgg(4)
                                        print "ROAR!!!!!!!"
                                else:
                                        print(servo.isMoving(0),servo.isMoving(1))
                        else:
                                print(servo.isMoving(0),servo.isMoving(1))
                

		# Play a random emotion if B Button is pressed	
		if j.X():
                        if j.leftBumper():
                                if j.rightBumper():
                                        emotion.easterEgg(2)
                                else:
                                        idleWait = time.time() + random.randint(2,10) #Next idle event wait time
                                        mode = "idle"
                                        emotion.Outburst()
                        else:
                                idleWait = time.time() + random.randint(2,10) #Next idle event wait time
                                mode = "idle"
                                emotion.Outburst()
                        
except:
	drivetrain.close()
	servo.close()
	j.close()
	raise
