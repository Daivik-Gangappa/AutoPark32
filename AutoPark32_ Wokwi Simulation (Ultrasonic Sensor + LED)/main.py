import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, time_pulse_us

# WiFi Credentials
SSID = "Wokwi-GUEST"
PASSWORD = ""

# MQTT Broker
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = b"smart_parking/status"

# Define 5 parking slots with GPIO pins
slots = [
    {"name": "A1", "trig": 5,  "echo": 18, "red": 15, "green": 14},
    {"name": "A2", "trig": 19, "echo": 21, "red": 22, "green": 23},
    {"name": "A3", "trig": 13, "echo": 12, "red": 27, "green": 26},
    {"name": "A4", "trig": 25, "echo": 33, "red": 32, "green": 4},
    {"name": "A5", "trig": 16, "echo": 17, "red": 2,  "green": 0}
]

# Initialize GPIOs
for slot in slots:
    slot["trig"] = Pin(slot["trig"], Pin.OUT)
    slot["echo"] = Pin(slot["echo"], Pin.IN)
    slot["red"] = Pin(slot["red"], Pin.OUT)
    slot["green"] = Pin(slot["green"], Pin.OUT)

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("WiFi Connected:", wlan.ifconfig())

# Connect to MQTT
def connect_mqtt():
    client = MQTTClient("esp32-client", MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT Broker:", MQTT_BROKER)
    return client

# Get distance from ultrasonic sensor
def get_distance(trig, echo):
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    duration = time_pulse_us(echo, 1, 30000)
    return (duration * 0.0343) / 2 if duration > 0 else 999

# Publish message to MQTT
def publish(client, slot_name, status):
    message = '{"slot": "' + slot_name + '", "status": "' + status + '"}'
    client.publish(MQTT_TOPIC, message)
    print(" ", message)

# --- Main Execution ---
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    for slot in slots:
        dist = get_distance(slot["trig"], slot["echo"])
        print(f" Slot {slot['name']} Distance: {dist:.2f} cm")

        if dist < 10:
            slot["red"].on()
            slot["green"].off()
            publish(mqtt_client, slot["name"], "Occupied")
        else:
            slot["red"].off()
            slot["green"].on()
            publish(mqtt_client, slot["name"], "Available")

    time.sleep(5)
