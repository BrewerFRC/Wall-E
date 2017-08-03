from time import time
"""

    import pid
    # setup
    powerPID = pid.Pid( Kp, Ki, Kd, minCalc, maxCalc, startValue )
    # use
    motorPower = powerPID.calc(measuredSpeed, deltaTime)
    # to adjust PID parameters
    powerPID.target = 5
    powerPID.Kp = 0.75
    powerPID.min =-10

"""

class PID():

    """PID Controller"""

    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0, min=-99999.0, max=99999.0, target=0.0):
        """Initalize PID P, I and D contants, set allowable output range and
        establish target."""
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.min = min           #Calculated output minimum
        self.max = max           #Calculated output minimum
        self.target = target     #the value being sought
        # internal use variables for calc method
        self._prevTime = time()   #used to calculate delta time
        self._prevError = 0       #error between target and measure
        self._sumError = 0        #accumates error for integral calc
        self._output = target     #most recent output.  start at target.



    def calc(self, measure):
        """Caculate and return PID output for given measured value relative to the
        set target. Output will be constrained within range of Min and Max."""
        tm = time()
        dt = tm - self._prevTime
        self._prevTime = tm
        # Integral calc
        error = measure - self.target
        self._sumError += error * dt
        I = self._sumError
        # Derivative calc
        D = (error - self._prevError) / dt
        self._prevError = error
        # Output calc
        output = self.Kp*error + self.Ki*I + self.Kd*D
        self._output = max(min(output, self.max), self.min)
        # Remember error and time for next iteration
        return self._output

    def prevCalc(self):
        """Returns the previously calculated PID output."""
        return self._output

    def reset(self):
        """Reset the PID accumulators back to starting values"""
        self._prevError = 0
        self._sumError = 0
        self._prevTime = time()
