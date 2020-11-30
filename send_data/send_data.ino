#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

const char *ssid = "TP-Link_2E5C";
const char *password = "95957845";

double current, usage;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  connectToWifi();
}

void connectToWifi()
{
  WiFi.mode(WIFI_OFF); //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA); //This line hides the viewing of ESP as wifi hotspot

  WiFi.begin(ssid, password); //Connect to your WiFi router
  Serial.println("");

  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

String splitString(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++)
  {
    if (data.charAt(i) == separator || i == maxIndex)
    {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

String msg = "";

void loop()
{
  // put your main code here, to run repeatedly:
  if (Serial.available())
  {
    msg = "";
    while (Serial.available())
    {
      msg += char(Serial.read());
      delay(50);
    }
    current = splitString(msg, ';', 0).toDouble();
    usage = splitString(msg, ';', 1).toDouble();
    kirimDataKeServer();
    // Serial.print(msg);
  }
}

void kirimDataKeServer()
{
  HTTPClient http; //Declare object of class HTTPClient
  String postData;
  //Post Data
  postData = "current=";
  postData += current;
  postData += "&usage=";
  postData += usage;

  http.begin("http://hci-flask.run-ap-south1.goorm.io");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  int httpCode = http.POST(postData); //Send the request
  String payload = http.getString();  //Get the response payload

  Serial.println(httpCode); //Print HTTP return code
  Serial.println(payload);  //Print request response payload

  http.end();
}
