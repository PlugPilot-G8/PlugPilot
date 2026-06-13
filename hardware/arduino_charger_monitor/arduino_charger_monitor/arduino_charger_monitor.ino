#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const String CHARGER_ID = "CHG001";

const int BUTTON_PIN = 6;
const int RELAY_PIN = 2;
const int RELAY_ON_STATE = LOW;
const int RELAY_OFF_STATE = HIGH;

const int RED_PIN = 3;
const int YELLOW_PIN = 4;
const int GREEN_PIN = 7;

const unsigned long CODE_INTERVAL = 60000;
const unsigned long READY_INTERVAL = 3000;
const unsigned long BUTTON_DEBOUNCE = 50;

const int BUTTON_ACTIVE_STATE = LOW;

bool authorized = false;
bool reserved = false;
bool freeMode = false;
bool configured = false;
bool charging = false;

String currentCode = "";

unsigned long lastCodeTime = 0;
unsigned long lastReadyTime = 0;
unsigned long lastButtonChangeTime = 0;

int lastButtonReading = HIGH;
int stableButtonState = HIGH;

String currentScreenLine1 = "";
String currentScreenLine2 = "";

void setStatusLeds(bool red, bool yellow, bool green)
{
    digitalWrite(RED_PIN, red);
    digitalWrite(YELLOW_PIN, yellow);
    digitalWrite(GREEN_PIN, green);
}

void ledBlocked()
{
    setStatusLeds(true, false, false);
}

void ledReserved()
{
    setStatusLeds(false, true, false);
}

void ledFree()
{
    setStatusLeds(false, false, true);
}

void ledCharging()
{
    setStatusLeds(true, false, false);
}

void ledError()
{
    setStatusLeds(true, true, false);
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

String generateCode()
{
    return String(random(100000, 999999));
}

void setRelay(bool state)
{
    digitalWrite(RELAY_PIN, state ? RELAY_ON_STATE : RELAY_OFF_STATE);
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
    updateLCD("Uso liberado", "Aperte o botao");
    ledFree();
}

void showCharging()
{
    updateLCD("Carregador", "ocupado");
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
    charging = false;
    setRelay(false);

    showAuthorized();
}

void startCharging()
{
    authorized = true;
    charging = true;
    setRelay(true);

    Serial.print("HARDWARE:");
    Serial.print(CHARGER_ID);
    Serial.println(":IN_USE");

    showCharging();
}

void stopCharging()
{
    authorized = false;
    charging = false;
    reserved = false;
    freeMode = true;
    currentCode = "";
    setRelay(false);

    Serial.print("HARDWARE:");
    Serial.print(CHARGER_ID);
    Serial.println(":FREE");

    showFree();
}

void lockCharger()
{
    authorized = false;
    freeMode = false;
    charging = false;
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
        charging = false;
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
        charging = false;

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
        stopCharging();
    }
    else if (command == "STOP:" + CHARGER_ID)
    {
        lockCharger();
    }
    else if (command == "ERROR:" + CHARGER_ID)
    {
        authorized = false;
        charging = false;
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

    if (charging)
    {
        stopCharging();
        return;
    }

    if (authorized)
    {
        startCharging();
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
        startCharging();
    }
}

void setup()
{
    Serial.begin(9600);

    digitalWrite(RELAY_PIN, RELAY_OFF_STATE);
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(YELLOW_PIN, OUTPUT);

    setRelay(false);
    ledBlocked();

    lastButtonReading = digitalRead(BUTTON_PIN);
    stableButtonState = lastButtonReading;

    randomSeed(micros());

    lcd.init();
    lcd.backlight();

    updateLCD("PlugPilot", "Iniciando...");

    delay(2000);

    sendReady();

    lastCodeTime = millis();
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

    int buttonReading = digitalRead(BUTTON_PIN);

    if (buttonReading != lastButtonReading)
    {
        lastButtonChangeTime = now;
        lastButtonReading = buttonReading;
    }

    if (
        now - lastButtonChangeTime >= BUTTON_DEBOUNCE &&
        buttonReading != stableButtonState
    )
    {
        stableButtonState = buttonReading;

        if (stableButtonState == BUTTON_ACTIVE_STATE)
        {
            handleButtonPress();
        }
    }

    if (reserved && !authorized && !charging && now - lastCodeTime >= CODE_INTERVAL)
    {
        sendNewCode();
        lastCodeTime = now;

        showReserved();
    }

    if (!charging)
    {
        setRelay(false);
    }
}
