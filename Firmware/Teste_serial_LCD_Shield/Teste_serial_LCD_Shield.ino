//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                  Teste de comunicão Serial
//
//   build 17/09/2024 by Raul
//   v0.1 REV. 000
//   Arrduino IDE 2.3.3
//
//    Arduino Uno
//    LCD nKeypad Shild
//
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Bibliotecas
#include <LiquidCrystal.h>  // Inclui biblioteca "LiquidCristal.h"

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Definições
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);  // Define Pinos do Display

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variáveis
String RX;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Confiruração
void setup() {

  lcd.begin(16, 2);  // Estabelece caracteres do display
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  lcd.clear();
  lcd.print("Teste comunicacao");
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Loop Principal
void loop() {

  while (Serial.available()) {
    Serial.println(RX);

    RX = Serial.readString();  // read the incoming data as string
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Recebido: ");
    lcd.setCursor(0, 1);
    lcd.print(RX);
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Fim