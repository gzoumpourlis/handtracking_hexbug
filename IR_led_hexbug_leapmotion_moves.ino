#define HEXBUG_SPIDER_CHANNEL 'A'

// How many times does a rotation code needs to be send to complete a full
// turn? This number was made up based on experimentation.
#define HEXBUG_FULL_ROTATION 13 // 18
// The number of milliseconds to wait after sending an instruction. This number
// was also made up based on experimentation.
#define HEXBUG_DELAY_AFTER_INSTRUCTION 192
// IR codes and utilities for Hexbug Spider.
#include "hexbug_spider.h"

// Pin the IR LED is wired to. Must be a PWM pin.
#define PIN_IR_OUTPUT 3

char incomingByte;   // for incoming serial data

void setup(void)
{
  Serial.begin(9600);
  Serial.println("Make sure your HexBug spider is within the IR LED's range.");

  hexbug_spider_setup_pin(PIN_IR_OUTPUT);
}

void loop(void) {
  
  if (Serial.available() > 0) {
    
    incomingByte = Serial.read();
    Serial.print("Key pressed: ");
    Serial.println(incomingByte);
    
    if (incomingByte == 'a' || incomingByte == 'A'){
      // rotate left, x degrees (counter-clockwise)
      hexbug_spider_spin(-28);
    }
    
    if (incomingByte == 'd' || incomingByte == 'D'){
      // rotate right, x degrees (clockwise)
      hexbug_spider_spin(28);
    }
  
    if (incomingByte == 's' || incomingByte == 'S'){
      // go backward N times
      hexbug_spider_advance(-1);
    }
    
    if (incomingByte == 'w' || incomingByte == 'W'){
      // go forward N times
      hexbug_spider_advance(1);
    }
    
  }
  
}
