import maestro
import random

# Servo channels
CH_YAW = 2
CH_PITCH = 3
CH_BROW = 4
# Left/Right yaw constants
YAW_SPEED = 35
YAW_ACCELERATION = 7
YAW_L = 4378
YAW_CL = 5933
YAW_C = 6496
YAW_CR = 6895
YAW_R = 8200
# Up/Down pitch constants
PITCH_SPEED = 15
PITCH_ACCELERATION = 7
PITCH_U = 7007
PITCH_CU = 6591
PITCH_C = 6343
PITCH_CD = 6144
PITCH_D = 5706
# Brow Up/Down constants
BROW_SPEED = 30
BROW_U = 4032
BROW_C = 5100
BROW_D = 5952

#
# FUNCTIONS
#


# Test if x is within or on two points of a range
def between(x,limit1,limit2):
        if limit1 < limit2:
                return x >= limit1 and x <= limit2
        else:
                return x >= limit2 and x <= limit1

#
# HEAD CLASS
#

class Head():
        # Provide maestro controller obj
	def __init__(self, maestro):
		self.maestro = maestro
		#maestro.setRange(CH_YAW, YAW_R, YAW_L)
		#maestro.setRange(CH_PITCH, PITCH_U, PITCH_D)
		#maestro.setRange(CH_BROW, BROW_U, BROW_D)
		maestro.setAccel(CH_YAW, YAW_ACCELERATION)
		maestro.setAccel(CH_PITCH, PITCH_ACCELERATION)
        
        def _speedCalc(self, pitch, yaw,throttle=1.0):
                yaw_delta = abs(yaw - self.maestro.getPosition(CH_YAW))
                pitch_delta = abs(pitch - self.maestro.getPosition(CH_PITCH))
                if yaw_delta == 0:
                        yaw_delta += 1
                if pitch_delta == 0:
                        pitch_delta += 1
                yaw_time = float(yaw_delta) / YAW_SPEED * throttle
                pitch_time = float(pitch_delta) / PITCH_SPEED * throttle
                if yaw_time >= pitch_time:
                        spd_ratio = pitch_time / yaw_time
                        pitch_spd = int(spd_ratio * PITCH_SPEED * throttle)
                        return (int(pitch_spd), int(YAW_SPEED * throttle))
                else:
                        spd_ratio = yaw_time / pitch_time
                        yaw_spd = int(spd_ratio * YAW_SPEED * throttle)
                        return (int(PITCH_SPEED * throttle), int(yaw_spd))
                
	def isUp(self):
		return between(self.maestro.getPosition(CH_PITCH),PITCH_CU,PITCH_U)
	def isDown(self):
                return between(self.maestro.getPosition(CH_PITCH),PITCH_CD,PITCH_D)
	def isPitchCentered(self):
                return between(self.maestro.getPosition(CH_PITCH),PITCH_CU,PITCH_CD)
	def isLeft(self):
                return between(self.maestro.getPosition(CH_YAW),YAW_L,YAW_CL)
	def isRight(self):
                return between(self.maestro.getPosition(CH_YAW),YAW_R,YAW_CR)
	def isYawCentered(self):
                return between(self.maestro.getPosition(CH_YAW),YAW_CL,YAW_CR)
	def isBrowUp(self):
                return self.maestro.getPosition(CH_BROW) >= BROW_U
	def isBrowDown(self):
                return self.maestro.getPosition(CH_BROW) <= BROW_D
	def isBrowCentered(self):
                return self.maestro.getPosition(CH_BROW) == BROW_C
	def isPitchMoving(self):
                pass
	def isYawMoving(self):
                pass
	def isBrowMoving(self):
                pass
	def isHeadMoving(self):
                pass
        
	def movePitch(self, position, speed):
                self.maestro.setSpeed(CH_PITCH, speed)
                self.maestro.setTarget(CH_PITCH, position)
                
	def moveYaw(self, position, speed):
                self.maestro.setSpeed(CH_YAW, speed)
                self.maestro.setTarget(CH_YAW, position)
                
	def moveBrow(self, position):
                self.maestro.setSpeed(CH_BROW, BROW_SPEED)
                self.maestro.setTarget(CH_BROW, position)

        # Function to stop the movement of the head
        # Work in progress. Do not use.
        def stopHead(self)
                self.maestro.setSpeed(CH_YAW, 0)
                self.maestro.setSpeed(CH_PITCH, 0)

        def browUp(self):
                self.moveBrow(BROW_U)

        def browDown(self):
                self.moveBrow(BROW_D)

        def browCenter(self):
                self.moveBrow(BROW_C)

        # Move head to a random coordinate upward
	def lookUp(self, throttle = 1.0):
                yawChange = random.randint(-600, 600)
                yaw = self.maestro.getPosition(CH_YAW) + yawChange
                pitch = random.randint(PITCH_CU, PITCH_U)
                (p, y) = self._speedCalc(pitch, yaw, throttle)
                print p, y
                self.maestro.setSpeed(CH_YAW, y)
                self.maestro.setSpeed(CH_PITCH, p)
                self.maestro.setTarget(CH_YAW, yaw)
                self.maestro.setTarget(CH_PITCH, pitch)

        # Move head to a random coordinate downward
	def lookDown(self, throttle = 1.0):
                yawChange = random.randint(-600, 600)
                yaw = self.maestro.getPosition(CH_YAW) + yawChange
                pitch = random.randint(PITCH_D, PITCH_CD)
                (p, y) = self._speedCalc(pitch, yaw, throttle)
                print p, y
                self.maestro.setSpeed(CH_YAW, y)
                self.maestro.setSpeed(CH_PITCH, p)
                self.maestro.setTarget(CH_YAW, yaw)
                self.maestro.setTarget(CH_PITCH, pitch)
                
        # Move head to a random coordinate to the left     
	def lookLeft(self, throttle = 1.0):
                pitchChange = random.randint(-600, 600)
                pitch = self.maestro.getPosition(CH_PITCH) + pitchChange
                yaw = random.randint(YAW_L, YAW_CL)
                (p, y) = self._speedCalc(pitch, yaw, throttle)
                print p, y
                self.maestro.setSpeed(CH_YAW, y)
                self.maestro.setSpeed(CH_PITCH, p)
                self.maestro.setTarget(CH_YAW, yaw)
                self.maestro.setTarget(CH_PITCH, pitch)

        # Move head to a random coordinate to the right
	def lookRight(self, throttle = 1.0):
                pitchChange = random.randint(-600, 600)
                pitch = self.maestro.getPosition(CH_PITCH) + pitchChange
                yaw = random.randint(YAW_CR, YAW_R)
                (p, y) = self._speedCalc(pitch, yaw, throttle)
                print p, y
                self.maestro.setSpeed(CH_YAW, y)
                self.maestro.setSpeed(CH_PITCH, p)
                self.maestro.setTarget(CH_YAW, yaw)
                self.maestro.setTarget(CH_PITCH, pitch)

        # Set yaw to center position (horizontal axis)
        def yawCenter(self, throttle = 0.5):
                #pitch = random.randint(PITCH_D, PITCH_U)
                yaw = random.randint(YAW_CL, YAW_CR)
                (p, y) = self._speedCalc(pitch, yaw, throttle)
                print "lookCentered",p, y
                self.maestro.setSpeed(CH_YAW, y)
                #self.maestro.setSpeed(CH_PITCH, p)
                self.maestro.setTarget(CH_YAW, yaw)
                #self.maestro.setTarget(CH_PITCH, pitch)

        # Set pitch to center position (Vertical Axis)
        def pitchCenter(self, throttle = 0.5):
                pitch = random.randint(PITCH_D, PITCH_U)
                #yaw = random.randint(YAW_CL, YAW_CR)
                (p, y) = self._speedCalc(pitch, yaw, throttle)
                print "lookCentered",p, y
                #self.maestro.setSpeed(CH_YAW, y)
                self.maestro.setSpeed(CH_PITCH, p)
                #self.maestro.setTarget(CH_YAW, yaw)
                self.maestro.setTarget(CH_PITCH, pitch)

        # Return head to center position
	def lookCentered(self, throttle = 0.5):
                pitch = random.randint(PITCH_D, PITCH_U)
                yaw = random.randint(YAW_CL, YAW_CR)
                (p, y) = self._speedCalc(pitch, yaw, throttle)
                print "lookCentered",p, y
                self.maestro.setSpeed(CH_YAW, y)
                self.maestro.setSpeed(CH_PITCH, p)
                self.maestro.setTarget(CH_YAW, yaw)
                self.maestro.setTarget(CH_PITCH, pitch)

        # Move the head at a constant rate when joystick is pressed.
        def moveConstLR(self, direc):
                
        # Move the head at a constant rate when joystick is pressed.
        def moveConstUD(self, direc):

        # Set the head to an exact position corresponding to a joystick.
	def moveAbs(self, x, y):
                self.maestro.setSpeed(CH_YAW,YAW_SPEED)
		if x >= 0:
			mx = int(x * (YAW_R - YAW_C) + YAW_C)
			self.maestro.setTarget(CH_YAW, mx)
		else:
			mx = int(YAW_C + x * (YAW_C - YAW_L))
			self.maestro.setTarget(CH_YAW, mx)

		self.maestro.setSpeed(CH_PITCH,PITCH_SPEED)
		if y >= 0:
			my = int(y * (PITCH_U - PITCH_C) + PITCH_C)
			self.maestro.setTarget(CH_PITCH, my)
		else:
			my = int(PITCH_C + y * (PITCH_C - PITCH_D))
			self.maestro.setTarget(CH_PITCH, my)
		#print self.maestro.getPosition(CH_YAW), self.maestro.getPosition(CH_PITCH)
