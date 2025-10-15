// 🔹 Arduino Traffic Light with Buzzer & Serial Control

const int redLed = 8;        // External Red LED
const int greenLed = 9;      // External Green LED
const int inbuiltLed = 13;   // Inbuilt Arduino LED (for GREEN)
const int buzzer = 10;       // Buzzer connected to digital pin 10

void setup() {
  Serial.begin(9600);

  pinMode(redLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(inbuiltLed, OUTPUT);
  pinMode(buzzer, OUTPUT);

  // Start with RED ON, others OFF
  digitalWrite(redLed, HIGH);
  digitalWrite(greenLed, LOW);
  digitalWrite(inbuiltLed, LOW);
  digitalWrite(buzzer, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove any leading/trailing spaces or newlines

    if (command == "GREEN") {
      digitalWrite(greenLed, HIGH);     // External Green LED ON
      digitalWrite(inbuiltLed, HIGH);   // Inbuilt LED ON
      digitalWrite(redLed, LOW);        // Red LED OFF
      digitalWrite(buzzer, HIGH);       // Buzzer ON
    } 
    else if (command == "RED") {
      digitalWrite(greenLed, LOW);      // External Green LED OFF
      digitalWrite(inbuiltLed, LOW);    // Inbuilt LED OFF
      digitalWrite(redLed, HIGH);       // Red LED ON
      digitalWrite(buzzer, LOW);        // Buzzer OFF
    }
  }
}

// Red LED on pin 8

// Green LED on pin 9

// Inbuilt LED on pin 13

// ✅ Buzzer on pin 10

// GREEN signal triggers: green LEDs + buzzer

// RED signal triggers: red LED, turns others OFF