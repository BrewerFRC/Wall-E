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

  public int getTarget() {
    return motorTarget;
  }
  public void setTarget(int target) {
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
    potValue = readPot(ch);
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
}
