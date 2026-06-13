#include <FastLED.h>
#include <avr/pgmspace.h>
#include "video_data.h" // Include generated data file containing the video
#define LED_PIN     12  // Data pin for the LED strip
#define NUM_LEDS    256  // Number of LEDs in your strip
#define BRIGHTNESS  16 // Brightness level (0-255)
#define LED_TYPE    WS2812B // Type of LED strip
#define COLOR_ORDER GRB // Color order of the LEDs
#define FRAME_SIZE  96 // Size of the frames in bytes

CRGB leds[NUM_LEDS]; // Define the LED array

void setup() {
  // Initialize Serial
  Serial.begin(9600);

  // Initialize FastLED
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}

void loop() {
  for (int f = 0; f < pgm_read_byte(&NUM_FRAMES); f++) {
    // Create Buffer
    byte workingFrame[FRAME_SIZE];
    // Load frame into buffer
    loadFrame(f, workingFrame);
    // Display frame in buffer
    displayFrame(workingFrame);
    FastLED.show();

    // Wait to display next frame
    Serial.println(pgm_read_byte(&FRAME_RATE));
    delay(1000 / pgm_read_byte(&FRAME_RATE));
  }
}

// Loads specified frame from Flash Memory into provided SRAM buffer
void loadFrame(int frameIndex, byte buffer[]) {
  for (int i = 0; i < FRAME_SIZE; i++) {
    buffer[i] = pgm_read_byte(&FRAMES[frameIndex][i]);
  }
}

// Displays given frame
void displayFrame(byte frame[]) {
  for (int i = 0; i < 8 * FRAME_SIZE; i += 3) {
    int rgb[3];
    for (int ii = 0; ii < 3; ii++) {
      rgb[ii] = 255 * bitRead(frame[(i + ii) / 8], 7 - ((i + ii) % 8));
    }
    leds[(i + 1) / 3] = CRGB(rgb[0],rgb[1],rgb[2]);
  }
}
