from controllers import controllers
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

class Head:
        # Provide maestro controller obj
	def __init__(self):
        self.yaw = controllers.maestro.Channel(CH_YAW)
        self.pitch = controllers.maestro.Channel(CH_PITCH)
        self.brow = controllers.maestro.Channel(CH_BROW)

		self.yaw.setRange(YAW_R, YAW_L)
		self.pitch.setRange(PITCH_U, PITCH_D)
		self.brow.setRange(BROW_U, BROW_D)
		self.yaw.setAcceleration(YAW_ACCELERATION)
		self.pitch.setAcceleration(PITCH_ACCELERATION)

    def _speedCalc(self, pitch, yaw,throttle=1.0):
        yaw_delta = abs(yaw - self.yaw.getPosition())
        pitch_delta = abs(pitch - self.pitch.getPosition())
        if yaw_delta == 0:
            yaw_delta = 1
        if pitch_delta == 0:
            pitch_delta = 1
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
		return between(self.pitch.getPosition(),PITCH_CU,PITCH_U)
	def isDown(self):
        return between(self.pitch.getPosition(),PITCH_CD,PITCH_D)
	def isPitchCentered(self):
        return between(self.pitch.getPosition(),PITCH_CU,PITCH_CD)
	def isLeft(self):
        return between(self.yaw.getPosition(),YAW_L,YAW_CL)
	def isRight(self):
        return between(self.yaw.getPosition(),YAW_R,YAW_CR)
	def isYawCentered(self):
        return between(self.yaw.getPosition(),YAW_CL,YAW_CR)
	def isBrowUp(self):
        return self.brow.getPosition() >= BROW_U
	def isBrowDown(self):
        return self.brow.getPosition() <= BROW_D
	def isBrowCentered(self):
        return self.brow.getPosition() == BROW_C
	def isPitchMoving(self):
        pass
	def isYawMoving(self):
        pass
	def isBrowMoving(self):
        pass
	def isHeadMoving(self):
        pass

	def movePitch(self, position, speed):
        self.pitch.setSpeed(speed)
        self.pitch.setTarget(position)

	def moveYaw(self, position, speed):
        self.yaw.setSpeed(speed)
        self.yaw.setTarget(position)

	def moveBrow(self, position):
        self.brow.setSpeed(BROW_SPEED)
        self.mbrow.setTarget(position)

    def moveLocation(self, pitch, yaw):
        self.movePitch(pitch)
        self.moveYaw(yaw)

    # Function to stop the movement of the head
    # Work in progress. Do not use.
    def stopHead(self):
        self.moveBrow(self.brow.getPosition(), BROW_SPEED)
        self.moveYaw(self.yaw.getPosition(), YAW_SPEED)
        self.movePitch(self.pitch.getPosition(), PITCH_SPEED)

    def browUp(self):
        self.moveBrow(BROW_U)

    def browDown(self):
        self.moveBrow(BROW_D)

    def browCenter(self):
        self.moveBrow(BROW_C)

    # Move head to a random coordinate upward
	def lookUp(self, speed = 1.0):
        yaw = min(9000, max(3000, self.yaw.getPosition() + random.randint(-600, 600)))
        pitch = random.randint(PITCH_CU, PITCH_U)
        (pitchSpeed, yawSpeed) = self._speedCalc(pitch, yaw, speed)
        self.movePitch(pitch, pitchSpeed)
        self.moveYaw(yaw, yawSpeed)

    # Move head to a random coordinate downward
	def lookDown(self, speed = 1.0):
        yaw = min(9000, max(3000, self.yaw.getPosition() + random.randint(-600, 600)))
        pitch = random.randint(PITCH_D, PITCH_CD)
        (pitchSpeed, yawSpeed) = self._speedCalc(pitch, yaw, speed)
        self.movePitch(pitch, pitchSpeed)
        self.moveYaw(yaw, yawSpeed)

    # Move head to a random coordinate to the left
	def lookLeft(self, speed = 1.0):
        pitch = min(9000, max(3000, self.pitch.getPosition() + random.randint(-600, 600)))
        yaw = random.randint(YAW_L, YAW_CL)
        (pitchSpeed, yawSpeed) = self._speedCalc(pitch, yaw, speed)
        self.movePitch(pitch, pitchSpeed)
        self.moveYaw(yaw, yawSpeed)

    # Move head to a random coordinate to the right
	def lookRight(self, speed = 1.0):
        pitch = min(9000, max(3000, self.pitch.getPosition() + random.randint(-600, 600)))
        yaw = random.randint(YAW_CR, YAW_R)
        (pitchSpeed, yawSpeed) = self._speedCalc(pitch, yaw, speed)
        self.movePitch(pitch, pitchSpeed)
        self.moveYaw(yaw, yawSpeed)

    # Set yaw to center position (horizontal axis)
    def yawCenter(self, speed = 0.5):
        self.moveYaw(YAW_C, speed)

    # Set pitch to center position (Vertical Axis)
    def pitchCenter(self, speed = 0.5):
        self.movePitch(PITCH_C, speed)

    # Return head to center position
	def lookCentered(self, throttle = 0.5):
        (pitchSpeed, yawSpeed) = self._speedCalc(PITCH_C, YAW_C, speed)
        self.movePitch(PITCH_C, pitchSpeed)
        self.moveYaw(YAW_C, yawSpeed)

    # Move the head according to a winch style system.
    # Work in progress. Do not use
    def manualMove(self, x, y):
        # Have the head move left if joystick pushes left.
        # Have the head move right if joystick pushes right.
        # Otherwise, keep horizontal movement at current position.
        if x > 0.5:
            yawMove = yaw_R
        elif x < -0.5:
            yawMove = yaw_L
        else:
            yawMove = self.yaw.getPosition()

        # Have the head move up if joystick pushes up.
        # Have the head move down if joystick pushes down.
        # Otherwise, keep vertical movement at current position.
        if y > 0.5:
            pitchMove = pitch_U
        elif y < -0.5:
            pitchMove = pitch_D
        else:
            pitchMove = self.pitch.getPosition()

        # Move the head
        self.moveYaw(yawMove, YAW_SPEED)
        self.movePitch(pitchMove, PITCH_SPEED)

    # Set the head to an exact position corresponding to a joystick.
	def moveAbs(self, x, y):
        self.yaw.setSpeed(YAW_SPEED)
        if x >= 0:
            mx = int(x * (YAW_R - YAW_C) + YAW_C)
			self.yaw.setTarget(mx)
		else:
			mx = int(YAW_C + x * (YAW_C - YAW_L))
			self.yaw.setTarget(mx)

		self.pitch.setSpeed(PITCH_SPEED)
		if y >= 0:
			my = int(y * (PITCH_U - PITCH_C) + PITCH_C)
			self.pitch.setTarget(my)
		else:
			my = int(PITCH_C + y * (PITCH_C - PITCH_D))
			self.pitch.setTarget(my)
