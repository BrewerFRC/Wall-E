#include <Servo.h>
#define LEFT_POTENTIOMETER_PORT A1
#define RIGHT_POTENTIOMETER_PORT A3
#define ARM_LEFT_PORT 5
#define ARM_RIGHT_PORT 2
#define ARM_LEFT_MIN 460
#define ARM_LEFT_MAX 780
#define ARM_RIGHT_MIN 271
#define ARM_RIGHT_MAX 583

//const int POTMIN;
//const int POTMAX;
const double KP = 0.07;
const double MAXPOWER = 0.2;
const byte lineid = 255;
const float LEFT_SCALE = (ARM_LEFT_MAX - ARM_LEFT_MIN) / 45;
const float RIGHT_SCALE = (ARM_RIGHT_MAX - ARM_RIGHT_MIN) / 45;

int power = 90;
byte buffer[3];
int bufferpos = 0;



//int targetL = 20; //The target of the motor in degrees

class Arm{
  char name;
  int potport;
  int potmin;
  int motorchan;
  double scale;
  Servo motorobj;
  
  int pot;
  float degree;
  float target = 0.0;
  int motstartdir = 1;
  double pos0;
  public:
    
  Arm(char name, int potport, int potmin, double scale, int motorchan){
    this->name = name;  
    this->potport = potport;
    this->potmin = potmin;
    this->scale = scale;
    this->motorchan = motorchan;
  }
  
  void init() {
    Serial.println("Attaching Motor");
    motorobj.attach(motorchan);
    motorobj.write(100);
    Serial.println(motorobj.read());
    pos0 = toDegree(analogRead(potport), potmin, scale);
    
  }
    
  void update(){
      pot = analogRead(potport); 
      degree = toDegree(pot, potmin, scale);  // Convert pot reading to a relative degree angle
      // PID calculation to determine motor power required
      double error = target - degree;
      double output = KP * error;
      output = min(max(output, -1.0),1.0);   //constrain between -1.0 and +1.0
      output = output * MAXPOWER;
      double power = servoPower(output* motstartdir);
      //Serial.println(degreeL);
      /*
      Serial.print(name);
      Serial.print(" ");
      Serial.print(power);
      Serial.print(" ");
      Serial.print(degree);
      Serial.print(" ");
      Serial.println(pot);
      */
      
      motorobj.write(power);
    }
    
    void initCompleted () {
      if (pos0 - analogRead(potport) < 0){
        motstartdir = -1;
      }
    }
    void setTarget (float extinput){
      target = extinput;
    }
};

//Serial.begin(9600);
Arm ArmL = Arm('l', LEFT_POTENTIOMETER_PORT, ARM_LEFT_MIN, LEFT_SCALE, ARM_LEFT_PORT);
Arm ArmR = Arm('r', RIGHT_POTENTIOMETER_PORT, ARM_RIGHT_MIN, RIGHT_SCALE, ARM_RIGHT_PORT);

void setup (){
  Serial.begin(115200);
  Serial.println("Setup");
  ArmL.init();
  ArmR.init();
  delay(500);
  ArmL.initCompleted();
  ArmR.initCompleted();
}

void loop(){
  //Serial.println(degreeL);
  while(Serial.available()){
    buffer[bufferpos] = Serial.read();
    

    if(buffer[0] == lineid){
      //Serial.print("Length: ");
      //Serial.println(bufferpos);
      if(bufferpos == 2){
       char channel = buffer[bufferpos - 1];
       char comdegree = buffer[bufferpos];
       char degreest[3];
       itoa(comdegree, degreest, 10);
       Serial.print("Channel: ");
       Serial.println(channel == 'l');
       Serial.print("Degree: ");
       Serial.println(degreest);
        if(channel == 'l'){
          Serial.println("Targetted arm: " + channel);
          ArmL.setTarget(comdegree);
        } 
        else if (channel == 'r'){
          Serial.println("Targetted arm: " + channel);
          ArmR.setTarget(comdegree);
        }
       bufferpos = 0; 
       continue;
      }
      bufferpos += 1;
    }
    else{
        bufferpos = 0;
    }
  }
  ArmL.update();
  ArmR.update();

  
  //armL.write(power);
  /*
  Serial.print("Pot: ");
  Serial.print(potL);
  Serial.print(" Degree: ");
  Serial.print(degreeL);
  Serial.print(" Error: ");l
  Serial.print(error);
  Serial.print(" Power: ");
  Serial.print(error * KP);
  Serial.print(" Servo power: ");
  Serial.p
  rintln(power);
  */
  delay(20);
}



// Converts a percentage power (-1.0 to +1.0) to a servo power (0 to 180)
double servoPower(double powerInput){
  const double CENTER = 90;
  const double SCALE = 90;
  double Power = powerInput * SCALE + CENTER;
  return Power;
}

float toDegree(int pos, int xaxis, double scaler){
  return (pos - xaxis) / scaler;
}
