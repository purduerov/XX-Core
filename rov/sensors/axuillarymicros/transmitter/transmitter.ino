#include <avr/io.h>
#include <util/delay.h>

#define RINP PA7
#define FINP PB2
#define PDEL 11
void pulse(){
  
  //Idle
  PORTA &= ~(1 << RINP);
  PORTB &= ~(1 << FINP);
  _delay_us(PDEL);
  
  //Forward
  PORTA &= ~(1 << RINP);
  PORTB |= (1 << FINP);
  _delay_us(PDEL);

  //Idle
  PORTA &= ~(1 << RINP);
  PORTB &= ~(1 << FINP);
  _delay_us(PDEL);

  //Reverse
  PORTA |= (1 << RINP);
  PORTB &= ~(1 << FINP);
  _delay_us(PDEL);

  //Idle
  PORTA &= ~(1 << RINP);
  PORTB &= ~(1 << FINP);
  _delay_us(PDEL);
}

void setup() {
DDRA |= (1 << PA6);

DDRA &= ~(1 << PA3);
DDRA &= ~(1 << RINP);
DDRB &= ~(1 << FINP);

PORTA |= (1 << PA3);
PORTA |= (1 << RINP);
PORTB |= (1 << FINP);
}

void loop() {
  if (bit_is_clear(PINA,PA3)){
    pulse();
    PORTA |= (1 << PA6);
  }else{
    PORTA &= ~(1 << PA6);
  }
}

