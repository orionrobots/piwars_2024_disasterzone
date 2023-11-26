import paho.mqtt.client as mqtt
from src.robot import Robot
from random import randint
import time

robot = Robot()
class MotorService:
    last_contact = 0

service = MotorService()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("motors/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "motors/forward":
        robot.forward()
        service.last_contact = time.monotonic()
    elif msg.topic == "motors/backward":
        robot.backward()
        service.last_contact = time.monotonic()

service_name = "motors"
username, password = "robot", "robot"
host, port = "localhost", 9001
client = mqtt.Client(client_id=f"{service_name}_{randint(0, 1000)}", transport="websockets")

client.username_pw_set(username, password)

print("Connecting")
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)

while True:
    client.loop()
    if time.monotonic() > service.last_contact + 1:
        robot.stop()
