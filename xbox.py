""" Xbox 360 controller support for Python
Published: 11/9/2013 - Steven Jacobs
Updated: 7/13/2017 - Connor Billings
This class module supports reading a connected xbox controller.
It requires that xboxdrv be installed first:
    sudo apt-get install xboxdrv
See http://pingus.seul.org/~grumbel/xboxdrv/ for details on xboxdrv
Example usage:
    import xbox
    joy = xbox.Joystick()         #Initialize joystick
    
    if joy.A():                   #Test state of the A button (1=pressed, 0=not pressed)
        print 'A button pressed'
    x_axis   = joy.leftX()        #X-axis of the left stick (values -1.0 to 1.0)
    (x,y)    = joy.leftStick()    #Returns tuple containing left X and Y axes (values -1.0 to 1.0)
    trigger  = joy.rightTrigger() #Right trigger position (values 0 to 1.0)
    
    joy.close()                   #Cleanup before exit
"""

import subprocess
import os
import select
import time

class Joystick:

    """Initializes the joystick/wireless receiver, launching 'xboxdrv' as a subprocess
    and checking that the wired joystick or wireless receiver is attached.
    The refreshRate determines the maximnum rate at which events are polled from xboxdrv.
    Calling any of the Joystick methods will cause a refresh to occur, if refreshTime has elapsed.
    Routinely call a Joystick method, at least once per second, to avoid overfilling the event buffer.
 
    Usage:
        joy = xbox.Joystick()
    """
    def __init__(self,refreshRate = 30):
        # Edge Trigger Booleans
        self.pressA = False
        self.pressB = False
        self.pressX = False
        self.pressY = False
        self.pressLT = False
        self.pressRT = False
        self.pressLB = False
        self.pressRB = False
        self.pressLTS = False
        self.pressRTS = False
        self.pressDPU = False
        self.pressDPD = False
        self.pressDPL = False
        self.pressDPR = False
        self.pressRJU = False
        self.pressRJD = False
        self.pressRJL = False
        self.pressRJR = False
        
        self.proc = subprocess.Popen(['xboxdrv','--no-uinput','--detach-kernel-driver'], stdout=subprocess.PIPE)
        self.pipe = self.proc.stdout
        #
        self.connectStatus = False  #will be set to True once controller is detected and stays on
        self.reading = '0' * 140    #initialize stick readings to all zeros
        #
        self.refreshTime = 0    #absolute time when next refresh (read results from xboxdrv stdout pipe) is to occur
        self.refreshDelay = 1.0 / refreshRate   #joystick refresh is to be performed 30 times per sec by default
        #
        # Read responses from 'xboxdrv' for upto 2 seconds, looking for controller/receiver to respond
        found = False
        waitTime = time.time() + 2
        while waitTime > time.time() and not found:
            readable, writeable, exception = select.select([self.pipe],[],[],0)
            if readable:
                response = self.pipe.readline()
                # Hard fail if we see this, so force an error
                if response[0:7] == 'No Xbox':
                    raise IOError('No Xbox controller/receiver found')
                # Success if we see the following
                if response[0:12] == 'Press Ctrl-c':
                    found = True
                # If we see 140 char line, we are seeing valid input
                if len(response) == 140:
                    found = True
                    self.connectStatus = True
                    self.reading = response
        # if the controller wasn't found, then halt
        if not found:
            self.close()
            raise IOError('Unable to detect Xbox controller/receiver - Run python as sudo')

    """Used by all Joystick methods to read the most recent events from xboxdrv.
    The refreshRate determines the maximum frequency with which events are checked.
    If a valid event response is found, then the controller is flagged as 'connected'.
    """
    def refresh(self):
        # Refresh the joystick readings based on regular defined freq
        if self.refreshTime < time.time():
            self.refreshTime = time.time() + self.refreshDelay  #set next refresh time
            # If there is text available to read from xboxdrv, then read it.
            readable, writeable, exception = select.select([self.pipe],[],[],0)
            if readable:
                # Read every line that is availabe.  We only need to decode the last one.
                while readable:
                    response = self.pipe.readline()
                    # A zero length response means controller has been unplugged.
                    if len(response) == 0:
                        raise IOError('Xbox controller disconnected from USB')
                    readable, writeable, exception = select.select([self.pipe],[],[],0)
                # Valid controller response will be 140 chars.  
                if len(response) == 140:
                    self.connectStatus = True
                    self.reading = response
                else:  #Any other response means we have lost wireless or controller battery
                    self.connectStatus = False

    """Return a status of True, when the controller is actively connected.
    Either loss of wireless signal or controller powering off will break connection.  The
    controller inputs will stop updating, so the last readings will remain in effect.  It is
    good practice to only act upon inputs if the controller is connected.  For instance, for
    a robot, stop all motors if "not connected()".
    
    An inital controller input, stick movement or button press, may be required before the connection
    status goes True.  If a connection is lost, the connection will resume automatically when the
    fault is corrected.
    """
    def connected(self):
        self.refresh()
        return self.connectStatus

    # Left stick X axis value scaled between -1.0 (left) and 1.0 (right) with deadzone tolerance correction
    def leftX(self,deadzone=4000):
        self.refresh()
        raw = int(self.reading[3:9])
        return self.axisScale(raw,deadzone)

    # Left stick Y axis value scaled between -1.0 (down) and 1.0 (up)
    def leftY(self,deadzone=4000):
        self.refresh()
        raw = int(self.reading[13:19])
        return self.axisScale(raw,deadzone)

    # Right stick X axis value scaled between -1.0 (left) and 1.0 (right)
    def rightX(self,deadzone=4000):
        self.refresh()
        raw = int(self.reading[24:30])
        return self.axisScale(raw,deadzone)

    # Right stick Y axis value scaled between -1.0 (down) and 1.0 (up)
    def rightY(self,deadzone=4000):
        self.refresh()
        raw = int(self.reading[34:40])
        return self.axisScale(raw,deadzone)

    # Right Joystick edge triggers
    # These functions return when their respective direction is > 0.8
    def whenRightJoystickUp(self):
        if self.rightY() > 0.8 and not self.pressRJU: # Set boolean and return true on rising edge
            self.pressRJU = True
            return True
        elif self.rightY() > 0.8 and self.pressRJU:
            return False
	else: # Reset boolean on falling edge
            self.pressRJU = False
	    return False
	
    def whenRightJoystickDown(self):
        if self.rightY() < -0.8 and not self.pressRJD: # Set boolean and return true on rising edge
            self.pressRJD = True
            return True
        elif self.rightY() < -0.8 and self.pressRJD:
            return False
	else: # Reset boolean on falling edge
            self.pressRJD = False
	    return False
	
    def whenRightJoystickLeft(self):
        if self.rightX() < -0.8 and not self.pressRJL: # Set boolean and return true on rising edge
            self.pressRJL = True
            return True
        elif self.rightX() < -0.8 and self.pressRJL:
            return False
	else: # Reset boolean on falling edge
            self.pressRJL = False
	    return False
	
    def whenRightJoystickRight(self):
        if self.rightX() > 0.8 and not self.pressRJR: # Set boolean and return true on rising edge
            self.pressRJR = True
            return True
        elif self.rightX() > 0.8 and self.pressRJR:
            return False
	else: # Reset boolean on falling edge
            self.pressRJR = False
	    return False

    # Scale raw (-32768 to +32767) axis with deadzone correcion
    # Deadzone is +/- range of values to consider to be center stick (ie. 0.0)
    def axisScale(self,raw,deadzone):
        if abs(raw) < deadzone:
            return 0.0
        else:
            if raw < 0:
                return (raw + deadzone) / (32768.0 - deadzone)
            else:
                return (raw - deadzone) / (32767.0 - deadzone)

    # Dpad Up status - returns 1 (pressed) or 0 (not pressed)
    def dpadUp(self):
        self.refresh()
        return int(self.reading[45:46])
    # Returns true on the rising edge of a Dpad Up press.
    def whenDpadUp(self):
        if self.dpadUp() and not self.pressDPU: # Set boolean and return true on rising edge
            self.pressDPU = True
            return True
        elif self.dpadUp() and self.pressDPU:
            return False
	else: # Reset boolean on falling edge
            self.pressDPU = False
	    return False
        
    # Dpad Down status - returns 1 (pressed) or 0 (not pressed)
    def dpadDown(self):
        self.refresh()
        return int(self.reading[50:51])
    # Returns true on the rising edge of a Dpad Down press.
    def whenDpadDown(self):
        if self.dpadDown() and not self.pressDPD: # Set boolean and return true on rising edge
            self.pressDPD = True
            return True
        elif self.dpadDown() and self.pressDPD:
            return False
	else: # Reset boolean on falling edge
            self.pressDPD = False
	    return False
	
    # Dpad Left status - returns 1 (pressed) or 0 (not pressed)
    def dpadLeft(self):
        self.refresh()
        return int(self.reading[55:56])
    # Returns true on the rising edge of a Dpad Left press.
    def whenDpadLeft(self):
        if self.dpadLeft() and not self.pressDPL: # Set boolean and return true on rising edge
            self.pressDPL = True
            return True
        elif self.dpadLeft() and self.pressDPL:
            return False
	else: # Reset boolean on falling edge
            self.pressDPL = False
	    return False
        
    # Dpad Right status - returns 1 (pressed) or 0 (not pressed)
    def dpadRight(self):
        self.refresh()
        return int(self.reading[60:61])
    # Returns true on the rising edge of a Dpad Right press.
    def whenDpadRight(self):
        if self.dpadRight() and not self.pressDPR: # Set boolean and return true on rising edge
            self.pressDPR = True
            return True
        elif self.dpadRight() and self.pressDPR:
            return False
	else: # Reset boolean on falling edge
            self.pressDPR = False
	    return False
        
    # Back button status - returns 1 (pressed) or 0 (not pressed)
    def Back(self):
        self.refresh()
        return int(self.reading[68:69])

    # Guide button status - returns 1 (pressed) or 0 (not pressed)
    def Guide(self):
        self.refresh()
        return int(self.reading[76:77])

    # Start button status - returns 1 (pressed) or 0 (not pressed)
    def Start(self):
        self.refresh()
        return int(self.reading[84:85])

    # Left Thumbstick button status - returns 1 (pressed) or 0 (not pressed)
    def leftThumbstick(self):
        self.refresh()
        return int(self.reading[90:91])
    # Returns true on the rising edge of a leftThumbstick button press.
    def whenLeftThumbstick(self):
        if self.leftThumbstick() and not self.pressLTS: # Set boolean and return true on rising edge
            self.pressLTS = True
            return True
        elif self.leftThumbstick() and self.pressLTS:
            return False
	else: # Reset boolean on falling edge
            self.pressLTS = False
	    return False

    # Right Thumbstick button status - returns 1 (pressed) or 0 (not pressed)
    def rightThumbstick(self):
        self.refresh()
        return int(self.reading[95:96])
    # Returns true on the rising edge of a rightThumbstick button press.
    def whenRightThumbstick(self):
        if self.rightThumbstick() and not self.pressRTS: # Set boolean and return true on rising edge
            self.pressRTS = True
            return True
        elif self.rightThumbstick() and self.pressRTS:
            return False
	else: # Reset boolean on falling edge
            self.pressRTS = False
	    return False

    # A button status - returns 1 (pressed) or 0 (not pressed)
    def A(self):
        self.refresh()
        return int(self.reading[100:101])
    # Returns true on the rising edge of an A button press.
    def whenA(self):
        if self.A() and not self.pressA: # Set boolean and return true on rising edge
            self.pressA = True
            return True
        elif self.A() and self.pressA:
            return False
	else: # Reset boolean on falling edge
            self.pressA = False
	    return False
        
        
    # B button status - returns 1 (pressed) or 0 (not pressed)
    def B(self):
        self.refresh()
        return int(self.reading[104:105])
    # Returns true on the rising edge of a B button press.
    def whenB(self):
        if self.B() and not self.pressB: # Set boolean and return true on rising edge
            self.pressB = True
            return True
        elif self.B() and self.pressB:
            return False
	else: # Reset boolean on falling edge
            self.pressB = False
	    return False
                
    # X button status - returns 1 (pressed) or 0 (not pressed)
    def X(self):
        self.refresh()
        return int(self.reading[108:109])
    # Returns true on the rising edge of an X button press.
    def whenX(self):
        if self.X() and not self.pressX: # Set boolean and return true on rising edge
            self.pressX = True
            return True
        elif self.X() and self.pressX:
            return False
	else: # Reset boolean on falling edge
            self.pressX = False
	    return False

    # Y button status - returns 1 (pressed) or 0 (not pressed)
    def Y(self):
        self.refresh()
        return int(self.reading[112:113])
    # Returns true on the rising edge of a Y button press.
    def whenY(self):
        if self.Y() and not self.pressY: # Set boolean and return true on rising edge
            self.pressY = True
            return True
        elif self.Y() and self.pressY:
            return False
	else: # Reset boolean on falling edge
            self.pressY = False
	    return False

    # Left Bumper button status - returns 1 (pressed) or 0 (not pressed)
    def leftBumper(self):
        self.refresh()
        return int(self.reading[118:119])
    # Returns true on the rising edge of a leftBumper press.
    def whenLeftBumper(self):
        global pressLB
        if self.leftBumper() and not self.pressLB: # Set boolean and return true on rising edge
            self.pressLB = True
            return True
        elif self.leftBumper() and self.pressLB:
            return False
	else: # Reset boolean on falling edge
            self.pressLB = False
	    return False

    # Right Bumper button status - returns 1 (pressed) or 0 (not pressed)
    def rightBumper(self):
        self.refresh()
        return int(self.reading[123:124])
    # Returns true on the rising edge of a rightBumper press.
    def whenRightBumper(self):
        if self.rightBumper() and not self.pressRB: # Set boolean and return true on rising edge
            self.pressRB = True
            return True
        elif self.rightBumper() and self.pressRB:
            return False
	else: # Reset boolean on falling edge
            self.pressRB = False
	    return False

    # Left Trigger value scaled between 0.0 to 1.0
    def leftTrigger(self):
        self.refresh()
        return int(self.reading[129:132]) / 255.0
    # Returns true on the rising edge of a left trigger press.
    def whenLeftTrigger(self):
        if self.leftTrigger() > 0.3 and not self.pressLT: # Set boolean and return true on rising edge
            self.pressLT = True
            return True
        elif self.leftTrigger() > 0.3 and self.pressLT:
            return False
	else: # Reset boolean on falling edge
            self.pressLT = False
	    return False
        
    # Right trigger value scaled between 0.0 to 1.0
    def rightTrigger(self):
        self.refresh()
        return int(self.reading[136:139]) / 255.0
    # Returns true on the rising edge of a right trigger press.
    def whenRightTrigger(self):
        if self.rightTrigger() > 0.3 and not self.pressRT: # Set boolean and return true on rising edge
            self.pressRT = True
            return True
        elif self.rightTrigger() > 0.3 and self.pressRT:
            return False
	else: # Reset boolean on falling edge
            self.pressRT = False
	    return False

    # Returns tuple containing X and Y axis values for Left stick scaled between -1.0 to 1.0
    # Usage:
    #     x,y = joy.leftStick()
    def leftStick(self,deadzone=4000):
        self.refresh()
        return (self.leftX(deadzone),self.leftY(deadzone))

    # Returns tuple containing X and Y axis values for Right stick scaled between -1.0 to 1.0
    # Usage:
    #     x,y = joy.rightStick() 
    def rightStick(self,deadzone=4000):
        self.refresh()
        return (self.rightX(deadzone),self.rightY(deadzone))

    # Cleanup by ending the xboxdrv subprocess
    def close(self):
        os.system('pkill xboxdrv')
