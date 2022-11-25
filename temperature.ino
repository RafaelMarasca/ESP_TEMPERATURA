/**
 * Projeto: Temperatura ESP32 + Python
 * Descrição: Obtem a temperatura e manda via serial para o computador
 */

#define T_PIN 34 //Pino de temperatura 

const float beta = 3380; //Define o valor de beta do NTC10k
const float t0 = (25 + 273.16); //25º em Kelvin
const float R0 = 10000.0; //Resistencia em 25º
const float R1 = 10000.0; //Resisteencia de 10k em série com o NTC10k


//Calcula a temperatura estimada
float get_temperature(float voltage)
{
   float Rth = R1*((3.3/voltage) - 1);
   return ((beta*t0)/(t0*log(Rth/R0) + beta)) - 273.16;
}

void setup()
{
  Serial.begin(115200);
}

void loop()
{

  float voltage = analogRead(T_PIN)*3.3/4095.0; //Converte o a leitura do ADC para um valor de tensão
  float temperature = get_temperature(voltage); //Obtem a temperatura
  
  Serial.println(temperature); //Envia via serial
} 
