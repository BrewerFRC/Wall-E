import head
import random
import pygame
import maestro
import xbox
import drive
import time

#VARIABLES

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

class Emotions:
        def __init__(self, head):
                self.head = head

        #
        # EMOTION OPTIONS
        #:
        def happy(self):
            playSnd("Chatter 2.mp3")
            self.head.browCenter()
            self.head.lookCentered()


        def curious(self):
            self.head.lookCentered()
            self.head.browCenter()


        def sad(self):
            playSnd("Ohhhh.mp3")
            self.head.browDown()
            self.head.lookDown()
            self.head.lookLeft()


        def pissed(self):
            playSnd("Motor whir.mp3")
            self.head.browUp()
            self.head.lookCentered()
            print "WALL-E isn't happy with you."
            #time.sleep(0.5)
            #playSnd("Jitters.mp3")

        def startled(self):
            playSnd("Whoohoo.mp3")
            self.head.lookCentered()
            self.head.browCenter()

        def intro(self):
            self.head.lookUp()
            self.head.browCenter()
            #playSnd("Walle Name.mp3")
            playSnd ("Walle Name.mp3")

        # function to select an emotion
        def Outburst(self):
                selectEm = random.randint(0,5)
                if selectEm == 0:
                        self.happy()
                elif selectEm == 1:
                        self.curious()
                elif selectEm == 2:
                        self.sad()
                elif selectEm == 3:
                        self.pissed()
                elif selectEm == 4:
                        self.startled()
                else:
                        self.intro()
                print selectEm

        # BAD WOLF
        def easterEgg(self, btn):
                if btn == 1: #Y
                        self.head.lookCentered()
                        self.head.lookUp()
                        self.head.browUp()
                        playSnd("Yowl.mp3")
                        self.head.lookLeft()
                        time.sleep(.5)
                        self.head.lookCentered()
                        time.sleep(.5)
                        self.head.lookRight()
                        time.sleep(.5)
                        self.head.lookCentered()
                        time.sleep(.5)
                        self.head.lookLeft()
                        time.sleep(.5)
                        self.head.lookCentered()
                        time.sleep(.5)
                        self.head.lookRight()
                        time.sleep(.5)
                        self.head.lookCentered()
                        time.sleep(.5)
                        self.head.lookLeft()
                elif btn == 2: #X
                        self.head.lookUp()
                        self.head.browCenter()
                        playSnd("Tadaa.mp3")
                elif btn == 3: #B
                        self.head.lookUp()
                        playSnd("Motor whir.mp3")
                        time.sleep(.2)
                        playSnd("Motor whir.mp3")
                        self.head.lookCentered()
                        time.sleep(.3)
                        self.head.lookDown()
                        playSnd("Motor whir.mp3")
                        time.sleep(.2)
                        playSnd("Motor whir.mp3")
                        self.head.lookCentered()
                        time.sleep(.3)
                        self.head.lookUp()
                        playSnd("Motor whir.mp3")
                        time.sleep(.2)
                        playSnd("Motor whir.mp3")
                        self.head.lookCentered()
                        time.sleep(.3)
                        self.head.lookDown()
                        playSnd("Motor whir.mp3")
                        time.sleep(.2)
                        playSnd("Motor whir.mp3")
                        time.sleep(.3)
                        #Add easterEgg() for B
                else: #btn == 4 #A
                        playSnd("ROAR.mp3")
                        time.sleep(.2)
                        playSnd("ROAR.mp3")
