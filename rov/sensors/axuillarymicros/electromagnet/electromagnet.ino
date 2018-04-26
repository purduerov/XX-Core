// import No Design 2013 MCP3008 library

#include <Wire.h>
#define  ELECTROPIN PD3 
//define pin connections

bool state = false;
void setup() {
  PORTD |= (1 << ELECTROPIN);
  // put your setup code here, to run once:
  Wire.begin(0x2B);
  Wire.onRequest(setelectro);
}

void setelectro() {
        if(state) {
               //Turn Electromagnet On 
               PORTD |= (1 << ELECTROPIN);
               Wire.write(1);
        }else{
               //Turn Electromagnet off 
               PORTD &= ~(1 << ELECTROPIN);
               Wire.write(0);
        }
        state = ~state;
}
void loop() {
}

