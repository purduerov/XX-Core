/*// import No Design 2013 MCP3008 library

#include <MCP3008.h>
#include <Wire.h>
 /*
//define pin connections

#define CS_PIN1 7
#define CS_PIN2 8
#define CS_PIN3 12
#define CS_PIN4 13
//consider using ICSP instead of these pins

#define CLOCK_PIN 9
#define MOSI_PIN 11
#define MISO_PIN 10
 
MCP3008 adc1(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN1);
MCP3008 adc2(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN2);
MCP3008 adc3(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN3);
MCP3008 adc4(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN4);

void setup() {
  // put your setup code here, to run once:
  Wire.begin(0x76);
  Wire.onRequest(writeData);
}

void loop() {
  
}

void writeData() {
  Wire.write(1);
  Wire.write(2);/*
  for (int i=0; i < 8; i++) {
//    int val1 = adc1.readADC(i);
   // Wire.write(8);
  }

  for (int i = 0; i < 8; i++) {
  //  int val2 = adc2.readADC(i);
    //Wire.write(val2);
  }

  for (int i = 0; i < 8; i++) {
    //int val3 = adc3.readADC(i);
    //Wire.write(val3);
  }

  for (int i = 0; i < 8; i++) {
  //  int val4 = adc4.readADC(i);
   // Wire.write(val4);
  }
  
}
*/

// i2c/wiring proof of concept code - tie two Arduinos together via
// i2c and do some simple data xfer.
//
// slave side code
//
// Jason Winningham (kg4wsv)
// 14 jan 2008

#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

void setup() {
pinMode(13, OUTPUT);
Serial.begin(9600); // start serial for output
// initialize i2c as slave
Wire.begin(SLAVE_ADDRESS);

// define callbacks for i2c communication
Wire.onReceive(receiveData);
Wire.onRequest(sendData);

}

void loop() {
delay(100);
}

// callback for received data
void receiveData(int byteCount){

while(Wire.available()) {
number = Wire.read();
//Serial.print(“data received: “);
Serial.println(number);

if (number == 1){

if (state == 0){
digitalWrite(13, HIGH); // set the LED on
state = 1;
}
else{
digitalWrite(13, LOW); // set the LED off
state = 0;
}
}
}
}

// callback for sending data
void sendData(){
Wire.write(number);
}
