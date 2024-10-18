#include <LiquidCrystal.h>  // Inclui biblioteca "LiquidCristal.h"

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);  // Define Pinos do Display

int Menu = 0;    // Inicializa valores para Menu
int estado = 0;  // Inicializa valores para estado

void clearPrintTitle();

void setup() {
  lcd.begin(16, 2);  // Estabelece caracteres do display
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(13, OUTPUT);
  clearPrintTitle();
  Serial.print("V0.1");
}

void loop() {
  Comunicacao();
    delay(1);
}

void clearPrintTitle() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Teste comunicação");
}


void Comunicacao() {
  if (Serial.available() > 0) {

    int dado = Serial.read();
    lcd.clear();
    lcd.setCursor(0, 1);
    lcd.println("recebio " + dado);
    Serial.print("recebio " + dado);

    if (dado == '1') {

       digitalWrite(LED_BUILTIN, HIGH); 
    } else if (dado == '0') {

       digitalWrite(LED_BUILTIN, LOW); 
    }
  }
}
