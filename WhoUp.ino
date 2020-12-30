int i = 0;
#define COLOR_MAX (255)
#define NUM_STATES (7)

struct Color {
  unsigned char r;
  unsigned char g;
  unsigned char b;
};

struct StateColor {
  struct Color color;
  char name;
  bool active;
};

struct Color off = {0, 0, 0};
struct Color red = {COLOR_MAX, 0, 0};
struct Color green = {0, COLOR_MAX, 0};
struct Color blue = {0, 0, COLOR_MAX};
struct Color cyan = {0, COLOR_MAX, };
struct Color magenta = {COLOR_MAX, 0, COLOR_MAX};
struct Color yellow = {COLOR_MAX, COLOR_MAX, 0};
struct Color white = {COLOR_MAX, COLOR_MAX, COLOR_MAX};

struct StateColor states[NUM_STATES] = {
  {red, 'r', false},
  {green, 'g', false},
  {blue, 'b', false},
  {cyan, 'c', false},
  {magenta, 'm', false},
  {yellow, 'y', false},
  {white, 'w', false}
}; 

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (states[i].active) {
    updateLed(states[i].color);
    delay(1000);
  }

  i = (i + 1) % NUM_STATES;
}

void serialEvent() {
  while (Serial.available()) {
    char incomingByte = (char) Serial.read();
    int j = 0;
    for (j = 0; j < NUM_STATES; j++) {
      if (states[j].name == incomingByte) {
        incomingByte = (char) Serial.read();
        if (incomingByte == '+') {
          states[j].active = true;
        } else if (incomingByte == '-') {
          states[j].active = false;
        }
      }
    } 
  }
}

void updateLed(struct Color color) {
  analogWrite(11, color.r);
  analogWrite(12, color.g);
  analogWrite(13, color.b);
}