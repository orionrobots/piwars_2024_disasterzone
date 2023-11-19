# import ssl

import paho.mqtt.client as mqtt

from robot_settings import Settings

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("drive_motors/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

settings = Settings()
print("Creating client")
client = mqtt.Client(client_id="drive_motors",
                     transport="websockets",
                     protocol=mqtt.MQTTv31)
print("Setting username")
client.username_pw_set(username=settings.mqtt_username, password=settings.mqtt_password)
# print("Setting TLS")
# client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED)

print("Setting callbacks")
client.on_connect = on_connect
client.on_message = on_message
print("Connecting")
client.connect(settings.mqtt_host, settings.mqtt_port)

print("Starting loop")
while True:
    client.loop(0.1)
    # do background work here
    print("Background task")
