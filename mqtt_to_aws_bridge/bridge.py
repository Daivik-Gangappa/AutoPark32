import json
import ssl
from paho.mqtt.client import Client as HiveMQClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# --- HiveMQ MQTT Setup ---
HIVE_HOST = "test.mosquitto.org"
HIVE_PORT = 1883
HIVE_TOPIC = "smart_parking/status"

# --- AWS IoT Setup ---
AWS_HOST = "a3mm3pt1h8soxw-ats.iot.us-east-1.amazonaws.com"
AWS_TOPIC = "smart_parking/status"

CLIENT_ID = "BridgeClient"
PATH_ROOT_CA = "D:/IOT/AutoPark32/mqtt_to_aws_bridge/AmazonRootCA1.pem"
PATH_CERT = "D:/IOT/AutoPark32/mqtt_to_aws_bridge/f9c9d3037270bd48bacd5a72cd808b18ae55e7b8391840263334e74eba2e34cf-certificate.pem.crt"
PATH_PRIVATE_KEY = "D:/IOT/AutoPark32/mqtt_to_aws_bridge/f9c9d3037270bd48bacd5a72cd808b18ae55e7b8391840263334e74eba2e34cf-private.pem.key"

# --- AWS IoT MQTT Client ---
aws_client = AWSIoTMQTTClient(CLIENT_ID)
aws_client.configureEndpoint(AWS_HOST, 8883)
aws_client.configureCredentials(PATH_ROOT_CA, PATH_PRIVATE_KEY, PATH_CERT)
aws_client.configureOfflinePublishQueueing(-1)
aws_client.configureDrainingFrequency(2)
aws_client.configureConnectDisconnectTimeout(10)
aws_client.configureMQTTOperationTimeout(5)
aws_client.connect()

# --- HiveMQ to AWS Forwarder ---
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"[HiveMQ →] {payload}")
        aws_client.publish(AWS_TOPIC, payload, 1)
        print(f"[→ AWS IoT]  Forwarded")
    except Exception as e:
        print(" Error forwarding:", e)

# --- HiveMQ Subscriber Client ---
hive_client = HiveMQClient()
hive_client.on_message = on_message
hive_client.connect(HIVE_HOST, HIVE_PORT)
hive_client.subscribe(HIVE_TOPIC)
hive_client.loop_forever()
