class Controller {
  Motor motor;
  int acceleration = 1024;
  int targetSpeed;
  int speed = 1024;
  int target;

  public:
  Controller(int channel, int speed, int acceleration) {
    motor = Motor(channel, 100, 1000);
    this.targetSpeed = speed;
    this.acceleration = acceleration;
  }

  public int getPosition() {
    return this.motor.readPot();
  }

  //Set acceleration in "potentiometer steps / cycles^2".
  void setAcceleration(int acceleration) {
    this.acceleration = acceleration;
  }

  //Set speed in "potentiometer steps / cycles".
  void setSpeed(int speed) {
    this.targetSpeed = speed;
  }

  //Set minimum position from 0-1023.
  void setMin(int min) {
    this.motor.setMin(min);
  }

  //Set maximum position from 0-1023.
  void setMax(int max) {
    this.motor.setMax(max);
  }

  //Set target from 0-1023.
  void setTarget(int target) {
    this.target = target;
  }

  void update() {
    //If motor failed to initialize, return.
    if (!this.motor) {
      return;
    }

    //Calculate the error in target position
    int targetError = this.target - this.motor.getTarget();
    int targetSign = 1;
    if (targetError < 0) {
      sign = -1;
    }
    targetError = abs(targetError);

    //Calculate the error in speed and limit its change to acceleration
    int targetSpeed = this.targetSpeed;
    int n = this.speed / this.acceleration;
    if (targetError <= n * (n + 1) / 2 * acceleration) {
      targetSpeed = 0;
    }
    int speedError = this.targetSpeed - this.speed;
    int sign = 1;
    if (speedError < 0) {
      sign = -1;
    }
    speedError = abs(speedError);
    this.speed += sign*(min(this.acceleration, speedError)); 

    //Limit change change in target position to speed.
    m.setTarget(m.getTarget() + targetSign*(min(this.speed, targetError)))

    //Update components
    motor.update()
  }
}

