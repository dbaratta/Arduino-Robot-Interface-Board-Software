//Board = Arduino Uno
#define __AVR_ATmega328P__
#define ARDUINO 101
#define F_CPU 16000000L
#define __AVR__
extern "C" void __cxa_pure_virtual() {;}

//
//
void drive_motor(int motor_id, int direction, int speed);
void serial_rcv();
void process_cmd_string();

#include "C:\Program Files (x86)\arduino\hardware\arduino\variants\standard\pins_arduino.h" 
#include "C:\Program Files (x86)\arduino\hardware\arduino\cores\arduino\arduino.h"
#include "C:\Users\dbaratta\Documents\Arduino\ExplorersRover\ExplorersRover.ino"
