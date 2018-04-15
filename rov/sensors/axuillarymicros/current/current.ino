// import No Design 2013 MCP3008 library

#include <MCP3008.h>
#include <Wire.h>
 
//define pin connections

#define CS_PIN1 14
#define CS_PIN2 14
#define CS_PIN3 14
#define CS_PIN4 14
//consider using ICSP instead of these pins

#define CLOCK_PIN 17
#define MOSI_PIN 15
#define MISO_PIN 16
 
MCP3008 adc1(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN1);
MCP3008 adc2(CLOCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN2);
int currentdata[16];
int idx = 0;
int off = 0;
void setup() {
  // put your setup code here, to run once:
  Wire.begin(0x2B);
  Wire.onRequest(writeData);
}

void loop() {
    for (int i=0; i < 8; i++) {
    int val1 = adc1.readADC(i);
    //val1 = off + i;
    currentdata[i] = val1;
  }

/*  for (int i = 0; i < 8; i++) {
    int val2 = adc2.readADC(i);
    val2 = off + i + 8;
    currentdata[i+8] = val2;
  }*/
}

void writeData() {
      Wire.write(currentdata[idx]);
      ++idx;
      if(idx>=16){
        idx = 0;
      }
      off++;
}

