// import No Design 2013 MCP3008 library

#include <MCP3008.h>
#include <Wire.h>
 
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
  for (int i=0; i < 8; i++) {
    int val1 = adc1.readADC(i);
    Wire.write(val1);
  }

  for (int i = 0; i < 8; i++) {
    int val2 = adc2.readADC(i);
    Wire.write(val2);
  }

  for (int i = 0; i < 8; i++) {
    int val3 = adc3.readADC(i);
    Wire.write(val3);
  }

  for (int i = 0; i < 8; i++) {
    int val4 = adc4.readADC(i);
    Wire.write(val4);
  }
}

