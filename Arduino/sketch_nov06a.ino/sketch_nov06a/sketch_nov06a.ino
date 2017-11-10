int led = 13;

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  char leitura = Serial.read();
  if(leitura == '1'){
    digitalWrite(led, HIGH);
    Serial.println("Led ligado com sucesso");
  }else if(leitura == '0'){
    digitalWrite(led, LOW);
    Serial.println("Led desligado com sucesso");   
  }
}
