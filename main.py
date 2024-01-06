import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "laporan-perubahan-suhu"

sensor = dht.DHT22(Pin(15))

print("menyambungkan ke WiFi...", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.5)
print(" berhasil!")

print("meyambungkan ke MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("berhasil!")

prev_weather = ""
while True:
  print("Mengukur kondisi cuaca... ", end="")
  sensor.measure() 
  message = ujson.dumps({
    "suhu": sensor.temperature(),
    "kelembapan": sensor.humidity(),
  })
  if message != prev_weather:
    print("Updated!")
    print("mengirim ke MQTT topic {}: {}".format(MQTT_TOPIC, message))
    client.publish(MQTT_TOPIC, message)
    prev_weather = message
  else:
    print("Tidak Ada perubahan")
  time.sleep(1)
