#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "BAOS_2G";  
const char* password = "020801251000BO"; 

ESP8266WebServer server(80);

const int ledPin = D2; 

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  Serial.println("");
  Serial.print("Connecting to ");
  Serial.println(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  server.on("/", []() {
    server.send(200, "text/plain", "ESP8266 Web Server");
  });

  server.on("/ledon", []() {
    digitalWrite(ledPin, HIGH);
    server.send(200, "text/plain", "LED is ON");
  });

  server.on("/ledoff", []() {
    digitalWrite(ledPin, LOW);
    server.send(200, "text/plain", "LED is OFF");
  });

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
