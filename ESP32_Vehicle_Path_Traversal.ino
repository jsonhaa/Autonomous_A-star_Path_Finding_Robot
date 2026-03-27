#include <WiFi.h>
#include <vector>

WiFiServer server(8080);
WiFiClient client;
std::vector<char> directions;
bool sessionActive = false;

int motor1pin1 = 27, motor1pin2 = 26;
int motor2pin1 = 33, motor2pin2 = 25;
int pin1 = 18, pin2 = 19;
int dutyCycle = 125;

void stopMotors() {
  digitalWrite(motor1pin1, LOW); digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW); digitalWrite(motor2pin2, LOW);
  analogWrite(pin1, 0);
  analogWrite(pin2, 0);
}

void setup() {
  delay(2000);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin("Wifi-Name", "Password");    // For wifi, I am using 2.4 GHz, since the ESP32 does not support 5 GHz wifi.

  pinMode(motor1pin1, OUTPUT); pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT); pinMode(motor2pin2, OUTPUT);
  pinMode(pin1, OUTPUT); pinMode(pin2, OUTPUT);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.println(WiFi.localIP());
  server.begin();
  Serial.println("Server ready!");
}

void loop() {
  // look for new client if none
  if (!client || !client.connected()) {
    if (sessionActive) {
      // print directions from last session
      Serial.print("Full directions: ");
      for (int i = 0; i < directions.size(); i++) {
        Serial.print(directions[i]); Serial.print(" ");
      }
      Serial.println();
      directions.clear();
      sessionActive = false;
    }

    // properly close old connection
    client.stop();
    
    // wait for new connection
    client = server.available();
    if (client) {
      Serial.println("New client connected!");
      sessionActive = true;
    }
    return;
  }

  if (client.available()) {
    String cmd = client.readStringUntil('\n');
    cmd.trim();
    if (cmd.length() == 0) return;
    
    Serial.println("Got: " + cmd);
    directions.push_back(cmd[0]);

    if (cmd == "F") {
      digitalWrite(motor1pin1, HIGH); digitalWrite(motor1pin2, LOW);
      digitalWrite(motor2pin1, HIGH); digitalWrite(motor2pin2, LOW);
      analogWrite(pin1, dutyCycle - 7);
      analogWrite(pin2, dutyCycle);
      delay(500);
    } else if (cmd == "R") {
      digitalWrite(motor1pin1, LOW); digitalWrite(motor1pin2, HIGH);
      digitalWrite(motor2pin1, HIGH); digitalWrite(motor2pin2, LOW);
      analogWrite(pin1, dutyCycle);
      analogWrite(pin2, dutyCycle);
      delay(300);
    } else if (cmd == "L") {
      digitalWrite(motor1pin1, HIGH); digitalWrite(motor1pin2, LOW);
      digitalWrite(motor2pin1, LOW); digitalWrite(motor2pin2, HIGH);
      analogWrite(pin1, dutyCycle);
      analogWrite(pin2, dutyCycle);
      delay(300);
    }

    stopMotors();
    delay(300);
    client.println("OK");
    delay(100);
  }
}
