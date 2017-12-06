
/* Definição de portas */
int port_dht = 2;
int port_umid = 7;
int port_soil = A0;

/* Definição de pinos de dados */
int data_dht = 0;
int data_umid = 0;
int data_soil = 0;

/* Configuração de pinos de entrada de dados e
   taxa de transmissão */
void setup() {
  Serial.begin(9600);
  Serial.println("\n\n SOIL MOISTURE SENSOR\n");
  Serial.print("********************************\n\n");
  
  pinMode(port_dht, INPUT);
  pinMode(port_umid, INPUT);
  pinMode(port_soil, INPUT);
}

/* Leitura e captura contínua de dados 
   enviados pelos sensores - loop() */
void loop() {
  /* delay(ms) é dado em milisegundos. 1 ms = 0.001 s */
  delay(5000); // espera por 5 segundos
  
  /* leitura de dados */
  data_dht = analogRead(port_dht);
  data_umid = digitalRead(port_umid);  
  data_soil = analogRead(port_soil);
  
  Serial.println(data_dht); 
  Serial.print("\n\n");
  Serial.println(data_umid);
  Serial.println(data_soil);
  //tone(port_soil, 1, 1);
  // Serial.println(data_dht11_pin);  
  // Serial.println("------------------------------");
}



