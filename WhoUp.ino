/**
 * Accept inputs on serial port 9600
 * Lowercase character to add color (r = red)
 * Uppercase character to remove color
 * '-' to clear
 */

#define NUM_STATES (8)
#define DELAY (1000)

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

const struct Color off =     {0x00, 0x00, 0x00};
const struct Color red =     {0xFF, 0x00, 0x00};
const struct Color green =   {0x00, 0xFF, 0x00};
const struct Color blue =    {0x00, 0x00, 0xFF};
const struct Color cyan =    {0x00, 0xFF, 0xFF};
const struct Color magenta = {0xFF, 0x00, 0xFF};
const struct Color yellow =  {0xFF, 0x40, 0x00};
const struct Color white =   {0xFF, 0x60, 0x60};
const struct Color pink =    {0xFF, 0x10, 0x10};

struct StateColor states[NUM_STATES] = {
  {red,     'r', false},
  {green,   'g', false},
  {blue,    'b', false},
  {cyan,    'c', false},
  {magenta, 'm', false},
  {yellow,  'y', false},
  {white,   'w', false},
  {pink,    'p', false},
}; 

void setup() {
  Serial.begin(9600);

  // flash red on initialization
  updateLed(red);
  delay(DELAY / 4);
  updateLed(off);
  delay(DELAY / 4);
  updateLed(red);
  delay(DELAY / 4);
  updateLed(off);
  delay(DELAY / 4);
}

int i = 0;
bool hasColor = false;

void loop() {
  if (states[i].active) {
    updateLed(states[i].color);
    hasColor = true;
    delay(DELAY);
  }

  i++;
  if (i >= NUM_STATES) {
    if (!hasColor) {
      updateLed(off);
      delay(DELAY);
    }
    hasColor = false;
    i = 0;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char incomingByte = (char) Serial.read();
    int j = 0;
    // remove all colors
    if (incomingByte == '-') {
      for (j = 0; j < NUM_STATES; j++) {
        states[j].active = false;
      }
    }
    // add or remove a new color to the cycle
    else {
      char byteLower = tolower(incomingByte);
      for (j = 0; j < NUM_STATES; j++) {
        if (states[j].name == byteLower) {
          states[j].active = states[j].name == incomingByte;
        }
      }
    }
  }
}

void updateLed(struct Color color) {
  analogWrite(10, color.r);
  analogWrite(11, color.g);
  analogWrite(12, color.b);
}
