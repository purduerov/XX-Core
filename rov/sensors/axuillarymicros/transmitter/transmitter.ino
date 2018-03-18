#define INPUT_PIN 10
void onTransmit(){
  
}
void offTransmit(){
  
}
void setup() {
   pinMode(4,OUTPUT);  
   pinMode(INPUT_PIN,INPUT);
}

void loop() {
if(digitalRead(INPUT_PIN)){
        digitalWrite(4,HIGH);
}else{
        digitalWrite(4,LOW);
}
  
}

