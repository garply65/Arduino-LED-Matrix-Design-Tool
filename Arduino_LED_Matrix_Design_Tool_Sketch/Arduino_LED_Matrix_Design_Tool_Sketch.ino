#include <FastLED.h>
#define LED_PIN     12  // Data pin for the LED strip
#define NUM_LEDS    256  // Number of LEDs in your strip
#define BRIGHTNESS  16 // Brightness level (0-255)
#define LED_TYPE    WS2812B // Type of LED strip
#define COLOR_ORDER GRB // Color order of the LEDs
// Replace this with the text from the excel file.
#define PATTERN "--W---------------------------------W--------------------W------------------------G-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

CRGB leds[NUM_LEDS]; // Define the LED array

void setup() {
  // Initialize FastLED
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  for (int i = 0; i < NUM_LEDS; i++) {
    setColor(i);
  }
  FastLED.show();
}
void loop() {
  
}

void setColor(int ledNum) {
  int newLedNum = ledNum;
  int rowNum = (int)ledNum/8;
  if (rowNum % 2 != 0){
    newLedNum = ledNum + (7 - (2 *(ledNum % 8)));
  } 
  
  char color = PATTERN[ledNum];
  if (color == 'R') {
    leds[newLedNum] = CRGB::Red;
  } else if (color == 'G') {
    leds[newLedNum] = CRGB::Green;
  } else if (color == 'B') {
    leds[newLedNum] = CRGB::Blue;
  } else if (color == 'W') {
    leds[newLedNum] = CRGB::White;
  } else {
    leds[newLedNum] = CRGB::Black;
  }
}
