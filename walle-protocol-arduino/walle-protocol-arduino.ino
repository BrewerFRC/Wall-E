#include <Servo.h>
Servo servo;

class Motor {
  
  int potValue;
  int potMax;
  int potMin;  
  int degreeScale;
  int motorTarget;
  int ch;
  double motorSpeed;
  double error;
  
  double p = 0.5;
  int minSpeed = 5;
  int deadzone = 4;
  
  public:
  Motor(int channel, int min, int max){
    potMax = max;
    potMin = min;
    ch = channel;
    servo.attach(channel + 2);
    Serial.println("Constructor completed");
  }
  Motor() {
    
  }

  int getTarget() {
    return motorTarget;
  }
  void setTarget(int target) {
    motorTarget = map(motorTarget, 0, 180, potMin, potMax);
    Serial.print("motorTarget set to ");
    Serial.println(motorTarget);
  }

  void setMin(int min) {
    potMin = min;
  }

  void setMax(int max) {
    potMax = max;
  }

  int readPot() {
    if (ch == 0) {
      return analogRead(A0);
    } else if (ch == 1) {
      return analogRead(A1);
    } else if (ch == 2) {
      return analogRead(A3);
    } else if (ch == 3) {
      return analogRead(A4);
    }
  }
  void update() {
    potValue = readPot();
    Serial.print("potValue ");
    Serial.println(potValue);
    
    error = ((motorTarget - potValue));
    
    if (abs(error) <= deadzone) {
      error = 0;
    }
  
    error = error * p;
    
    if (error > 90) {
      error = 90;
    } else if (error < -90) {
      error = -90;
    }
  //Check error went from -90 to 50 with weird scale
  //map error onto motorspeed
    motorSpeed = error + 90;
  
    if (motorSpeed <= minSpeed) {
      motorSpeed = minSpeed;
    }

    servo.write(motorSpeed);
    Serial.print("Setting motor to ");
    Serial.println(motorSpeed);
  }
};

class Controller {
  Motor motor;
  int acceleration = 1024;
  int targetSpeed;
  int speed = 1024;
  int target;

  public:
  Controller(int channel, int speed, int acceleration) {
    motor = Motor(channel, 100, 1000);
    this->targetSpeed = speed;
    this->acceleration = acceleration;
  }

  int getPosition() {
    return this->motor.readPot();
  }

  //Set acceleration in "potentiometer steps / cycles^2".
  void setAcceleration(int acceleration) {
    this->acceleration = acceleration;
  }

  //Set speed in "potentiometer steps / cycles".
  void setSpeed(int speed) {
    this->targetSpeed = speed;
  }

  //Set minimum position from 0-1023.
  void setMin(int min) {
    this->motor.setMin(min);
  }

  //Set maximum position from 0-1023.
  void setMax(int max) {
    this->motor.setMax(max);
  }

  //Set target from 0-1023.
  void setTarget(int target) {
    this->target = target;
  }

  void update() {
    //If motor failed to initialize, return.

    //Calculate the error in target position
    int targetError = this->target - this->motor.getTarget();
    int targetSign = 1;
    if (targetError < 0) {
      targetSign = -1;
    }
    targetError = abs(targetError);

    //Calculate the error in speed and limit its change to acceleration
    int targetSpeed = this->targetSpeed;
    int n = this->speed / this->acceleration;
    if (targetError <= n * (n + 1) / 2 * acceleration) {
      targetSpeed = 0;
    }
    int speedError = this->targetSpeed - this->speed;
    int sign = 1;
    if (speedError < 0) {
      sign = -1;
    }
    speedError = abs(speedError);
    this->speed += sign*(min(this->acceleration, speedError)); 

    //Limit change change in target position to speed.
    motor.setTarget(motor.getTarget() + targetSign*(min(this->speed, targetError)));

    //Update components
    motor.update();
  }
};



void setup() {
  Serial.begin(115200);
}



void readCommand() {
  int command[5];
  int pos = 0;

  while(Serial.available() and pos < 5) {
    command[pos] = Serial.read();
    pos++;
  }

  //Decompose command
  char action = (char)command[0];
  int channel = command[1];
  String val = "";
  for (int i = 2;i < sizeof(command);i++) {
    val += (char)command[i];
  }
  int value = val.toInt();
  Controller c = getController(channel);
  
  //Read command
  if (action == "T") {
    c.setTarget(value);
  }
  else if (action == "S") {
    c.setSpeed(value);
  }
  else if (action == "A") {
    c.setAcceleration(value);
  }
  else if (action == "P") {
    Serial.print("P" + channel + String(min(999, c.getPosition())));
  }
  else if (action == "M") {
    c.setMax(value);
  }
  else if (action == "m") {
    c.setMin(value);
  }
}

Controller ch0(0, 1024, 20);
Controller ch1(1, 1024, 20);
Controller ch2(2, 1024, 20);
Controller ch3(3, 1024, 20);

Controller getController(int channel) {
  if (channel == 0) {
    return ch0;
  }
  else if (channel == 1) {
    return ch1;
  }
  else if (channel == 2) {
    return ch2;
  }
  else if (channel == 3) {
    return ch3;
  }
  return ch1;
}

void update() {
  ch0.update();
  ch1.update();
  ch2.update();
  ch3.update();
}

void loop() {
  readCommand();
  update();
  delay(20);
}
