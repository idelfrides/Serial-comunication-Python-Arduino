int led = 13;

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop() {
    delay(3000);
    digitalWrite(led, HIGH);
    Serial.println("Led ligado com sucesso");
    
    delay(3000);
    digitalWrite(led, LOW);
    Serial.println("Led desligado com sucesso");   
}

