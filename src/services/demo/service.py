import paho.mqtt.client as mqtt
from random import randint

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("demo/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

service_name = "demo"
username, password = "robot", "robot"
host, port = "localhost", 9001
client = mqtt.Client(client_id=f"{service_name}_{randint(0, 1000)}", transport="websockets")

client.username_pw_set(username, password)

print("Connecting")
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)
client.loop_forever()
