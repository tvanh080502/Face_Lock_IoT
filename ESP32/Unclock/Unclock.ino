#include <WiFi.h>
#include <ESP32Servo.h>

#define SERVO 13

// Update these with values suitable for your network.
const char* ssid = "Vanh";
const char* password = "123456789";

WiFiServer server(80);

Servo myServo;

void setup() {
  Serial.begin(115200);

  myServo.attach(SERVO);

  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Nhận khuôn mặt thành công");

    while (client.connected()) {
      if (client.available()) {
        String command = client.readStringUntil('\n');
        command.trim();
        if (command == "open") {
          myServo.write(90);
          delay(15000);
        } else {
          myServo.write(0);
        }
      } else {
        myServo.write(0);
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  } else {
    myServo.write(0);
  }
}