#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "SSID_NAME";
const char* password = "NETWORK_KEY";
const char* hostUrl = "YOUR_HOST_LINK_HERE";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(hostUrl);
    http.addHeader("Content-Type", "application/json");

    // Replace random values with actual sensor read pins
    String payload = "{\"temp\":92,\"rpm\":4000,\"vib\":0.12,\"bat\":12.6}";
    
    int response = http.POST(payload);
    http.end();
  }
  delay(5000); 
}
