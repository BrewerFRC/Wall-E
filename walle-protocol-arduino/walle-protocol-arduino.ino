Controller ch0(0, 1024, 20);
Controller ch1(1, 1024, 20);
Controller ch2(2, 1024, 20);
Controller ch3(3, 1024, 20);

void setup() {
  Serial.begin(115200);
}

void loop() {
  readCommand();
  update();
  delay(20);
}

public void update() {
  ch0.update();
  ch1.update();
  ch2.update();
  ch3.update();
}

public void readCommand() {
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
  if (c) {
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
      Serial.print("P" + channel + String(min(999, c.getPosition()));
    }
    else if (action == "M") {
      c.setMax(value);
    }
    else if (action == "m") {
      c.setMin(value);
    }
  }
}

public Controller getController(int channel) {
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
  return null;
}

