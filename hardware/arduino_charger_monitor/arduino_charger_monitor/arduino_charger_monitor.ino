const int BUTTON_PIN = 10;

const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 6;

bool ultimoEstado = false;

void setup() {

  Serial.begin(9600);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  setColor(0, 0, 255);

  Serial.println("SYSTEM:READY");
}

void setColor(int r, int g, int b) {
  analogWrite(RED_PIN, r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

void loop() {

  bool emUso = digitalRead(BUTTON_PIN) == LOW;

  if (emUso != ultimoEstado) {

    if (emUso) {

      Serial.println("CHARGER:1:IN_USE");

      setColor(255, 0, 0);

    } else {

      Serial.println("CHARGER:1:FREE");

      setColor(0, 255, 0);
    }

    ultimoEstado = emUso;
  }

  delay(50);
}