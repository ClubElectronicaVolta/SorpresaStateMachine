//Codigo para leer una rom y e imprimirla por consola serie. 
// por ahora hasta...256 bites

#define pin_A0  20
#define pin_A1  21
#define pin_A2  22
#define pin_A3  23
#define pin_A4  24
#define pin_A5  25
#define pin_A6  26
#define pin_A7  27
#define pin_A8  20
#define pin_A9  21
#define pin_A10  36
#define pin_A11  37
#define pin_A12  38
#define pin_A13  39
#define pin_A14  40


#define pin_D0  28
#define pin_D1  29
#define pin_D2  30
#define pin_D3  31
#define pin_D4  32
#define pin_D5  33
#define pin_D6  34
#define pin_D7  35

void setup() 
{
  
pinMode(pin_A0, OUTPUT);
pinMode(pin_A1, OUTPUT);
pinMode(pin_A2, OUTPUT);
pinMode(pin_A3, OUTPUT);
pinMode(pin_A4, OUTPUT);
pinMode(pin_A5, OUTPUT);
pinMode(pin_A6, OUTPUT);
pinMode(pin_A7, OUTPUT);
pinMode(pin_D0, INPUT);
pinMode(pin_D0, INPUT);
pinMode(pin_D0, INPUT);
pinMode(pin_D0, INPUT);
pinMode(pin_D0, INPUT);
pinMode(pin_D0, INPUT);
pinMode(pin_D0, INPUT);
pinMode(pin_D0, INPUT);

Serial.begin(9600);
Serial.println("Ok");
}

void loop() 
{
uint8_t datos[256];
uint8_t numero;
uint16_t filas, columnas;
uint8_t in_data;
uint16_t out_add;

Serial.print("*****");
for(columnas=0; columnas<0x10; columnas++)
  {
  Serial.print("|0");
  Serial.print(columnas,16);
  //Serial.print('|');
  }
Serial.print("\n\r");
for(filas=0; filas<0x1000; filas=filas+0x10)
  {
  if((filas & 0xF00)==0) 
    {
    Serial.print("|0");  //imprimo leading zero suprimido por el print
    if((filas & 0x0F0)==0) Serial.print('0');   //imprimo cero del medio suprimido por el print
    }
  else Serial.print("|");
  Serial.print(filas,16);
  Serial.print("|: ");
  for(columnas=0; columnas<0x10; columnas++)
    {
    // hago la composicion de ADDRESS para sacarla por los pines
    out_add=filas+columnas;
    if((out_add & 0x01)!=0) digitalWrite(pin_A0, HIGH); else digitalWrite(pin_A0, LOW);
    if((out_add & 0x02)!=0) digitalWrite(pin_A1, HIGH); else digitalWrite(pin_A1, LOW);
    if((out_add & 0x04)!=0) digitalWrite(pin_A2, HIGH); else digitalWrite(pin_A2, LOW);
    if((out_add & 0x08)!=0) digitalWrite(pin_A3, HIGH); else digitalWrite(pin_A3, LOW);
    if((out_add & 0x10)!=0) digitalWrite(pin_A4, HIGH); else digitalWrite(pin_A4, LOW);
    if((out_add & 0x20)!=0) digitalWrite(pin_A5, HIGH); else digitalWrite(pin_A5, LOW);
    if((out_add & 0x40)!=0) digitalWrite(pin_A6, HIGH); else digitalWrite(pin_A6, LOW);
    if((out_add & 0x80)!=0) digitalWrite(pin_A7, HIGH); else digitalWrite(pin_A7, LOW);   
    if((out_add & 0x100)!=0) digitalWrite(pin_A8,  HIGH); else digitalWrite(pin_A8, LOW);
    if((out_add & 0x200)!=0) digitalWrite(pin_A9,  HIGH); else digitalWrite(pin_A9, LOW);
    if((out_add & 0x400)!=0) digitalWrite(pin_A10, HIGH); else digitalWrite(pin_A10, LOW);
    if((out_add & 0x800)!=0) digitalWrite(pin_A11, HIGH); else digitalWrite(pin_A11, LOW);
    if((out_add & 0x1000)!=0) digitalWrite(pin_A12, HIGH); else digitalWrite(pin_A12, LOW);
    if((out_add & 0x2000)!=0) digitalWrite(pin_A13, HIGH); else digitalWrite(pin_A13, LOW);
    if((out_add & 0x4000)!=0) digitalWrite(pin_A14, HIGH); else digitalWrite(pin_A14, LOW);
    //hago la composicion de data
    if((digitalRead(pin_D0)!=0)) in_data  = 0x01; else in_data  =  0x00;
    if((digitalRead(pin_D1)!=0)) in_data |= 0x02; else in_data &= ~0x02;
    if((digitalRead(pin_D2)!=0)) in_data |= 0x04; else in_data &= ~0x04;
    if((digitalRead(pin_D3)!=0)) in_data |= 0x08; else in_data &= ~0x08;
    if((digitalRead(pin_D4)!=0)) in_data |= 0x10; else in_data &= ~0x10;
    if((digitalRead(pin_D5)!=0)) in_data |= 0x20; else in_data &= ~0x20;
    if((digitalRead(pin_D6)!=0)) in_data |= 0x40; else in_data &= ~0x40;
    if((digitalRead(pin_D7)!=0)) in_data |= 0x80; else in_data &= ~0x80;
    datos[filas+columnas]=in_data;    
    //-----------------------------------------------------------------
    if((numero=datos[filas+columnas]) <0x10) Serial.print('0'); //imprimo leading zero suprimido por el print
    Serial.print(numero,16);
    Serial.print(' ');
    }
  Serial.print("\n\r");
  }

while(1); // While eterno

}
