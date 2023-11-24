#include <WiFi.h>
#include <WebSocketsClient.h>

// WiFi credentials
const char *ssid = "Spider paul";
const char *password = "7500@@85";
unsigned long lastTime = 0;
unsigned long interval = 1000;
const int trigPin = 18;
const int echoPin = 19;
long distance, duration;

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length)
{
  switch (type)
  {
  case WStype_DISCONNECTED:
    Serial.printf("[WSc] Disconnected!\n");
    break;
  case WStype_CONNECTED:
    Serial.printf("[WSc] Connected to url: %s\n", payload);
    break;
  case WStype_TEXT:
    Serial.printf("[WSc] get text: %s\n", payload);
    break;
  }
}

void setup()
{
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");

  webSocket.begin("192.168.0.102", 3000, "/");

  webSocket.onEvent(webSocketEvent);

  webSocket.setReconnectInterval(5000);
}

void loop()
{
  webSocket.loop();
  unsigned long currentTime = millis();
  if (currentTime - lastTime > interval)
  {
    lastTime = currentTime;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);

    distance = duration * 0.034 / 2;

    webSocket.sendTXT(String(distance).c_str());
  }
}
