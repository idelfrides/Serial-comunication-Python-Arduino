/* inclisão de bibliotecas */
#include "DHT.h"

/* Definição de portas */
#define DHTPIN 2    
#define umidPin 2
#define soilPin A0

/* definindo o tipo de DHT a ser utilizado nesta app */
#define DHTTYPE DHT11  // DHT 11 

/* Definição e inicialização dos pinos de dados */
float data_dht = 0;
float data_umid = 0;
float data_soil = 0;
float data_dht_f = 0;

// Initialize DHT sensor for normal 16mhz Arduino
DHT dht(DHTPIN, DHTTYPE);
DHT dhtUmid(umidPin, DHTTYPE);

/* Configuração de pinos de entrada de dados e
   taxa de transmissão e inicializando a leitura */
void setup() {
  Serial.begin(9600);
  Serial.println("\n\n DHT11 AND SOIL MOISTURE SENSORS TEST\n");
  Serial.print("****************************************\n\n");
  
  //pinMode(port_dht, INPUT);
  pinMode(umidPin, INPUT);
  pinMode(soilPin, INPUT);

  dht.begin();
  dhtUmid.begin();
}

/* Leitura e captura contínua de dados 
   enviados pelos sensores - loop() 
   O método delay(ms) é dado em milisegundos.
   1 ms = 0.001 s = 1.10^-3 
   Espera por 5 s entre cada medidas/leitura */
void loop() {
  delay(2000); 
  
  /* leitura de dados */
  data_dht = dht.readTemperature();       // celcius
  data_umid = dhtUmid.readHumidity();  
  data_soil = analogRead(soilPin);
  data_dht_f = dht.readTemperature(true); // Fahrenheit

   /* verificação de dados lidos*/
  if (isnan(data_dht) || isnan(data_umid) || isnan(data_dht_f)){
    Serial.println("\nFailed to read from DHT sensor!");
    return;
  }
  if(isnan(data_soil)){
    Serial.println("\n Faile by reading soil moisture! \n");
    return;
  }else{
    /* impressão via monitor serial */
    
    /*Serial.print("\n TEMP FAHRENHEIT: "); 
    Serial.println(data_dht_f); 
    delay(2000); */
   
    Serial.print("\n TEMP CELCIUS: "); 
    Serial.println(data_dht); 
    delay(2000);
    
    Serial.print(" UMID: "); 
    Serial.println(data_umid);
    delay(2000);

    Serial.print(" UMID SOLO: "); 
    Serial.println(data_soil);
    Serial.print("\n-----------------------------");
  }
  
}


