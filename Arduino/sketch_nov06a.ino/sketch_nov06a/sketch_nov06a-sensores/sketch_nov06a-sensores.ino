int port_soil = A0;
//int port_dht11 = 2;

int data_soil_pin = 0; 
//int data_dht11_pin = 0; 

void setup() {
  Serial.begin(9600);

  Serial.println("SOIL MOISTURE SENSOR");
  pinMode(port_soil, INPUT);
  //pinMode(port_dht11, INPUT);
}

void loop() {
  delay(5000); // espera por 5 segundos
  data_soil_pin = analogRead(port_soil);
  //data_dht11_pin = digitalRead(port_dht11);  
  Serial.println(data_soil_pin); 
 // Serial.println(data_dht11_pin);  
  Serial.println("------------------------------");
}



