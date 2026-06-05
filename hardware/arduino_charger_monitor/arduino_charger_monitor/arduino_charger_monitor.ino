#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const String CHARGER_ID = "CHG001";

const int BUTTON_PIN = 4;
const int RELAY_PIN = 2;
const int ACS_PIN = A0;

const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 7;

// ACS712 5A
const float ACS_SENSITIVITY = 0.185;
const float CURRENT_THRESHOLD = 0.05;

const unsigned long CODE_INTERVAL = 60000;
const unsigned long CURRENT_INTERVAL = 1000;
const unsigned long READY_INTERVAL = 3000;
const unsigned long BUTTON_DEBOUNCE = 250;

const int BUTTON_ACTIVE_STATE = HIGH;

bool authorized = false;
bool reserved = false;
bool freeMode = false;
bool configured = false;

String currentCode = "";

unsigned long lastCodeTime = 0;
unsigned long lastCurrentTime = 0;
unsigned long lastReadyTime = 0;
unsigned long lastButtonTime = 0;

String currentScreenLine1 = "";
String currentScreenLine2 = "";

void setRGB(bool red, bool green, bool blue)
{
    digitalWrite(RED_PIN, red);
    digitalWrite(GREEN_PIN, green);
    digitalWrite(BLUE_PIN, blue);
}

void ledBlocked()
{
    setRGB(true, false, false);
}

void ledReserved()
{
    setRGB(true, true, false);
}

void ledFree()
{
    setRGB(false, true, false);
}

void ledCharging()
{
    setRGB(false, false, true);
}

void ledError()
{
    setRGB(true, false, true);
}

void updateLCD(String line1, String line2)
{
    if (line1 == currentScreenLine1 && line2 == currentScreenLine2)
    {
        return;
    }

    currentScreenLine1 = line1;
    currentScreenLine2 = line2;

    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print(line1);

    lcd.setCursor(0, 1);
    lcd.print(line2);
}

float readCurrent()
{
    long sum = 0;

    for (int i = 0; i < 100; i++)
    {
        sum += analogRead(ACS_PIN);
        delay(2);
    }

    float average = sum / 100.0;
    float voltage = average * (5.0 / 1023.0);
    float current = (voltage - 2.5) / ACS_SENSITIVITY;

    return abs(current);
}

String generateCode()
{
    return String(random(100000, 999999));
}

void setRelay(bool state)
{
    digitalWrite(RELAY_PIN, state ? HIGH : LOW);
}

void showFree()
{
    updateLCD("Livre", "Pressione botao");
    ledFree();
}

void showReserved()
{
    updateLCD("Reservado", "Codigo: " + currentCode);
    ledReserved();
}

void showAuthorized()
{
    updateLCD("LIBERADO", CHARGER_ID);
    ledFree();
}

void showCharging(float current)
{
    char currentText[17];
    dtostrf(current, 4, 2, currentText);

    updateLCD("EM USO", String(currentText) + " A");
    ledCharging();
}

void showBlocked()
{
    updateLCD("BLOQUEADO", "Use o App");
    ledBlocked();
}

void showError()
{
    updateLCD("ERRO SISTEMA", "Serial/Python");
    ledError();
}

void sendNewCode()
{
    currentCode = generateCode();

    Serial.print("CODE:");
    Serial.print(CHARGER_ID);
    Serial.print(":");
    Serial.println(currentCode);
}

void sendReady()
{
    Serial.print("READY:");
    Serial.println(CHARGER_ID);
}

void authorizeCharger()
{
    authorized = true;
    freeMode = false;
    setRelay(true);

    Serial.print("AUTHORIZED:");
    Serial.println(CHARGER_ID);

    showAuthorized();
}

void authorizeFreeUse()
{
    authorized = true;
    freeMode = true;
    setRelay(true);

    Serial.print("AUTHORIZED:");
    Serial.println(CHARGER_ID);

    updateLCD("USO LIBERADO", "Conecte veiculo");
    ledFree();
}

void lockCharger()
{
    authorized = false;
    freeMode = false;
    setRelay(false);

    Serial.print("LOCKED:");
    Serial.println(CHARGER_ID);

    if (reserved)
    {
        showReserved();
    }
    else
    {
        showBlocked();
    }
}

void handleCommand(String command)
{
    command.trim();

    if (command == "FREE:" + CHARGER_ID)
    {
        configured = true;
        reserved = false;
        authorized = false;
        freeMode = true;
        currentCode = "";

        setRelay(false);
        showFree();
    }
    else if (command == "RESERVED:" + CHARGER_ID)
    {
        configured = true;
        reserved = true;
        authorized = false;
        freeMode = false;

        setRelay(false);

        sendNewCode();
        lastCodeTime = millis();

        showReserved();
    }
    else if (command == "ALLOW:" + CHARGER_ID)
    {
        authorizeCharger();
    }
    else if (command == "DENY:" + CHARGER_ID)
    {
        lockCharger();
    }
    else if (command == "STOP:" + CHARGER_ID)
    {
        lockCharger();
    }
    else if (command == "ERROR:" + CHARGER_ID)
    {
        authorized = false;
        setRelay(false);

        showError();
    }
}

void handleButtonPress()
{
    if (!configured)
    {
        sendReady();
        updateLCD("Aguarde", "Sistema...");
        return;
    }

    if (authorized)
    {
        return;
    }

    if (reserved)
    {
        if (currentCode == "")
        {
            sendNewCode();
            lastCodeTime = millis();
        }

        showReserved();
        return;
    }

    if (freeMode)
    {
        authorizeFreeUse();
    }
}

void setup()
{
    Serial.begin(9600);

    pinMode(RELAY_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT);
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);

    setRelay(false);
    ledBlocked();

    randomSeed(analogRead(A1));

    lcd.init();
    lcd.backlight();

    updateLCD("PlugPilot", "Iniciando...");

    delay(2000);

    sendReady();

    lastCodeTime = millis();
    lastCurrentTime = millis();
    lastReadyTime = millis();

    updateLCD("Aguardando", "Sistema...");
}

void loop()
{
    unsigned long now = millis();

    if (Serial.available())
    {
        String command = Serial.readStringUntil('\n');
        handleCommand(command);
    }

    if (!configured && now - lastReadyTime >= READY_INTERVAL)
    {
        sendReady();
        lastReadyTime = now;
    }

    if (
        digitalRead(BUTTON_PIN) == BUTTON_ACTIVE_STATE &&
        now - lastButtonTime >= BUTTON_DEBOUNCE
    )
    {
        lastButtonTime = now;
        handleButtonPress();
    }

    if (reserved && !authorized && now - lastCodeTime >= CODE_INTERVAL)
    {
        sendNewCode();
        lastCodeTime = now;

        showReserved();
    }

    if (now - lastCurrentTime >= CURRENT_INTERVAL)
    {
        float current = readCurrent();

        if (authorized)
        {
            if (current > CURRENT_THRESHOLD)
            {
                Serial.print("CURRENT:");
                Serial.print(CHARGER_ID);
                Serial.print(":HIGH:");
                Serial.println(current, 3);

                showCharging(current);
            }
            else
            {
                Serial.print("CURRENT:");
                Serial.print(CHARGER_ID);
                Serial.print(":LOW:");
                Serial.println(current, 3);

                if (freeMode)
                {
                    showFree();
                }
                else
                {
                    showAuthorized();
                }
            }
        }

        lastCurrentTime = now;
    }

    if (!authorized)
    {
        setRelay(false);
    }
}
