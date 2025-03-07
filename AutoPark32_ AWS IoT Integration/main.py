import network
import time
import ujson
import machine
from umqtt.simple import MQTTClient
from machine import Pin, time_pulse_us

print("🚀 Starting ESP32 Simulation...")

# WiFi Credentials
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# AWS IoT Core MQTT Details
MQTT_BROKER = "a3m3p8th8soxw-ats.iot.us-east-1.amazonaws.com"  
MQTT_PORT = 8883
MQTT_TOPIC = "smart_parking/status"

# SSL/TLS Configuration - 
AWS_ROOT_CA = """-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
"""

AWS_CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIIDWTCCAkGgAwIBAgIUBBbi8yGfoTslZNSf3QkHtOHWBnQwDQYJKoZIhvcNAQEL
BQAwTTFLMEkGA1UECwxCQW1hem9uIFdlYiBTZXJ2aWNlcyBPPUFtYXpvbi5jb20g
SW5jLiBMPVNlYXR0bGUgU1Q9V2FzaGluZ3RvbiBDPVVTMB4XDTI1MDMwNzAzNDUy
OVoXDTQ5MTIzMTIzNTk1OVowHjEcMBoGA1UEAwwTQVdTIElvVCBDZXJ0aWZpY2F0
ZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKsK/BiWh8RQLuC6S5bw
4VsLrONqW3eOy+OpJad0fy/p6ngBfefg7hk3nXo7ZZnUJTPVmy+9UFk9HO5iHZMu
2KxqZtM2GY7N3oHCVeUhH2rewPE4nFZtUIMn/Np8ymeOmhncjYBTUIjdNPoD1qCv
UaJ+vu7WLUZyOEueTuUQP+ivw+uK9dUuo9ZKr8Y5kIjHHIOmyU71DIBOpg7R8ai1
ATUqJ+EhYuAihsYF0kH1Cqcqx51hE1A3DqI51XkATlgeGgjQsKQCjnA+L87EFdeM
ajOh+DoNhxZT7EjGTL/xGkp7emfBa3pEvePxHUQ2054I1eBSpGKV3lY10z4g9FLQ
JysCAwEAAaNgMF4wHwYDVR0jBBgwFoAUXX1H9CfCo/kjx/plsAOiOOK6QUwwHQYD
VR0OBBYEFKXi62Sye7Bz5nCYV6MLsWmsK1QIMAwGA1UdEwEB/wQCMAAwDgYDVR0P
AQH/BAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQBtFGtiQo3ZlRVENRjMWWD8SHGc
pgh2vuvw83vZWs/0FdiJD9vN4Tz5vZiz68MupjSG4qX3y8JizZ0LyNtCG0ZT9RkQ
zsLEGxlHXsZAlX9I4IeoSbj542qq/a4tgQ2UYjLzqk16BpWYq6PaGBYkN2y02dlF
2VuY18WiIS7UoZpqMlKVBNx6U8cBBj3o/z3Efdvutprd20H/yPnT4ppeiHBPmi+B
jV6a6yCBMq5Sq23fYJCSLeR04TePC/VJow5boQq681mzl1vmNcvxHQ1VMb52UQuh
Q/FzGFxuLFPSgi4ktbeiLSDjGB4kKf5oabDg6K1dIfdUCJfFVvVdQFMNoBqB
-----END CERTIFICATE-----
"""

AWS_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAqwr8GJaHxFAu4LpLlvDhWwus42pbd47L46klp3R/L+nqeAF9
5+DuGTedejtlmdQlM9WbL71QWT0c7mIdky7YrGpm0zYZjs3egcJV5SEfat7A8Tic
Vm1Qgyf82nzKZ46aGdyNgFNQiN00+gPWoK9Ron6+7tYtRnI4S55O5RA/6K/D64r1
1S6j1kqvxjmQiMccg6bJTvUMgE6mDtHxqLUBNSon4SFi4CKGxgXSQfUKpyrHnWET
UDcOojnVeQBOWB4aCNCwpAKOcD4vzsQV14xqM6H4Og2HFlPsSMZMv/EaSnt6Z8Fr
ekS94/EdRDbTngjV4FKkYpXeVjXTPiD0UtAnKwIDAQABAoIBAH1ldULVgT20h1ms
WuSTPrRQD/U+MUaqwuHqTTfCWciX1pUaiuLn7cdBFcvaJfesJ4Yj8T0DrxdtjXtb
JVGVg7aL30yzmfMvDRTWk8CDExR3sL5ogX1/cQpm06Ke4Ikha+rP3lGZQy7D9iXh
kIWHYvMdtv9EuDawYINX0YFv81qz5rrk+M2VbEMJjn2/0OJCCzzK3u7HUk+OIUDn
RVgqgIIjCaPU1d22jUCpG3yLBwFiV//p6ZRETrNn5XU2iTLBwhFfuF89N2aYGtek
gypPUcZWwEwpuvctL0zIPjX/6DYZ4nW3Q4yVTRa/xsLnYMa/thH3ikgqVFKy/Pjx
0CPhOoECgYEA0t8rC2gnb4UDuwYApGRiJFVp3fOOx5cijuhtCY9nkqvWDVTEiYOF
2WHgyuRxIeB13c/yChwRgd1Y+dBiJfh5we+m1I/aKoGY158J3qLnV/U6OT/4uIpa
Jhlb0KtZZSSp44M9zHGYeHstzCFsJuVeGQo710nh6oNRjII0kCA188ECgYEAz6XA
XI/Uh4uohuu4Ll1r750nHOOZzALeDO+Qp4vfr1rakhBf+RO+EvnWDf1w9wQcgtnr
AKrHHVEqGri+/MRI9QxD6QKiw1wan+jYeD81N7k7RNHSZt4SC+i8UF4GKeW57fo9
BFaSH1sFwCCqP94FD5KvZacWmDZGgHsF086upesCgYB80SwhbF0rXYh/w2XN6L1O
1F/9yJTS/1qtTFZ+OiwMXTouWeabnwYzTgRJFD8C1mHuEZAq+8JBJEvuUrJF13X6
nWgamauBTYSy3Khy5+oX3kfAa2VFll8V/hyiv0oC3FjTGnQR94tQhVjuYzopK8su
9yfEny7iKSi0Cr4iMW6+AQKBgQCmL48TxZ0f2ltHmDIxEV3ISOs7yMCXMZhLnBQW
s/CTJFCX4/kbnHxcLY3uZm9ZkvXKl+PoBcYUJZhgCIn6PJHzZRyYyR5A4l8AqldN
bbEG5v2TZ6ZP491noJ3OaGHgeFZlKwhYh3ytEak5iisXsHY2b3xnC+IechnczBju
2pSWfwKBgA1fm+NZqzUBW5upvAJe+Fhap4qyjZh2791sFEvuZTdYwYGmTr/1MWmY
yBHZ0I/bTkCSCaL7/Vi5ad4+XqEqH/fYreSw6gueLeDs/QimLbfB0ISdEAq54kCz
LSqbV5QBprzlztfjZBV5uRVzoZOPhzSYWWkHcIq9UDNwqi+hwN94
-----END RSA PRIVATE KEY-----
"""

print("✅ Certificates Loaded!")

# Define GPIO Pins
TRIG = Pin(5, Pin.OUT)  # Ultrasonic Trigger
ECHO = Pin(18, Pin.IN)  # Ultrasonic Echo
RED_LED = Pin(15, Pin.OUT)  # Red LED (Occupied)
GREEN_LED = Pin(14, Pin.OUT)  # Green LED (Available)

def connect_wifi():
    print("🌐 Scanning for Available Networks...")
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    networks = wlan.scan()  # Scan for available WiFi networks
    for net in networks:
        print(f"📡 Found Network: {net[0].decode()}")

    print("🌐 Connecting to WiFi...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    timeout = 20  # Timeout after 20 seconds
    while not wlan.isconnected():
        time.sleep(1)
        timeout -= 1
        print(".", end="")  # Show progress

        if timeout == 0:
            print("\n❌ WiFi Connection Failed! Restarting ESP32...")
            machine.reset()  # Restart ESP32

    print("\n✅ WiFi Connected!")

# Connect to AWS IoT Core via MQTT
def connect_mqtt():
    print("🔗 Connecting to AWS IoT...")

    try:
        ssl_params = {
            "cert": AWS_CERTIFICATE.encode(),  # Convert to bytes
            "key": AWS_PRIVATE_KEY.encode(),
            "cert_reqs": 2,  # Enforce certificate validation
            "ca_certs": AWS_ROOT_CA.encode()
        }

        client = MQTTClient(
            client_id="ESP32",
            server=MQTT_BROKER,
            port=MQTT_PORT,
            ssl=True,
            ssl_params=ssl_params
        )
        
        client.connect()
        print("✅ Connected to AWS IoT!")
        return client

    except Exception as e:
        print(f"❌ MQTT Connection Failed: {e}")
        machine.reset()

# Function to measure distance using Ultrasonic Sensor
def get_distance():
    print("📏 Measuring Distance...")
    
    TRIG.value(0)
    time.sleep_us(2)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)

    duration = time_pulse_us(ECHO, 1, 30000)  # Timeout after 30ms
    if duration < 0:
        print("⚠️ Error: No pulse received, setting distance to 1000cm")
        return 1000

    distance = (duration * 0.0343) / 2  # Convert to cm
    print(f"📏 Measured Distance: {distance} cm")
    return distance

# Send data to AWS IoT Core
def publish_status(client, slot_status):
    try:
        payload = ujson.dumps({"slot_status": slot_status})
        client.publish(MQTT_TOPIC, payload)
        print(f"📡 Sent to AWS IoT: {payload}")

    except Exception as e:
        print(f"❌ MQTT Publish Failed: {e}")

# Connect WiFi & Start Monitoring
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    distance = get_distance()
    
    if distance < 10:
        RED_LED.value(1)
        GREEN_LED.value(0)
        print("🚗 Parking Slot Occupied")
        publish_status(mqtt_client, "Occupied")
    
    else:
        RED_LED.value(0)
        GREEN_LED.value(1)
        print("🟢 Parking Slot Available")
        publish_status(mqtt_client, "Available")

    time.sleep(3)
