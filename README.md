#WIP Disregard everything in this README, final version should be done within a month
# Arduino-LED-Matrix-Design-Tool
This tool is intended to make designing and displaying images for the WS2812B LED Matrix for Arduino easier.

## Software Requirements
- Excel or Google Sheets
- Arduino IDE
## Usage Instructions
1. Download the excel file and Arduino sketch folder.
2. Move the sketch folder where ever you store your sketches.
3. To create design an image, open the excel file and edit the text in the grey shaded section of the spread sheet. W for white, R for red, G for green, and B for blue.
   ![Image Example](README_Images/Image_Example.png)
4. Copy the text in this cell ![Pattern Cell](README_Images/Pattern_Cell.png) and paste it into the PATTERN constant in the script file ![Pattern Constant](README_Images/Pattern_Constant.png).
5. Make sure that the LED_PIN constant is set to the data pin number you are using in your setup.
6. When you run the script after these steps the image you designed should show up on your LED Matrix.
## Dependencies
- FastLED
