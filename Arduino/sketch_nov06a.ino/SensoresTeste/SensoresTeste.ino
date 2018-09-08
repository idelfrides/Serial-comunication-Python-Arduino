/* inclusão de bibliotecas */
#include "DHT.h"

/* Definição de portas */
#define DHTPIN 2    // what pin we're connected to
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

/* Configuração de pinos de entrada de dados,
   taxa de transmissão e inicializando a leitura */
void setup() {
  Serial.begin(9600);
  pinMode(umidPin, INPUT);
  pinMode(soilPin, INPUT);
  dht.begin();
  dhtUmid.begin();
}

/* Leitura e captura contínua de dados 
   enviados pelos sensores - loop() 
   O método delay(ms) é dado em milisegundos.
   1ms = 0.001s = 1.10^-3 
   Espera por 5 s entre cada medida/leitura */
void loop() {
  delay(5000); 
  
  /* leitura de dados */
  data_dht = dht.readTemperature();       // celcius
  data_umid = dhtUmid.readHumidity();  
  data_soil = analogRead(soilPin);

  /* verificação de dados lidos*/
  if (isnan(data_dht) || isnan(data_umid)){
    Serial.println("\nFailed to read from DHT sensor!");
    return;
  }
  if(isnan(data_soil)){
    Serial.println("\n Faile by reading soil moisture! \n");
    return;
  }else{
    /* impressão via monitor serial */
    Serial.println(data_dht); 
    delay(2000);    
    /*Serial.println(data_umid);
    delay(2000);
    Serial.println(data_soil);  */  
  }
  
}


