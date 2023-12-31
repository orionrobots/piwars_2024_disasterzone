import explorerhat
import paho.mqtt.client as mqtt
from random import randint
import time
import json


class Motor():
    def __init__(self, board_motor :explorerhat.Motor):
        self._motor = board_motor
        self._throttle = 0
        
    def forward(self, speed: float=1):
        self.value = speed

    def backward(self, speed: float=1):
        self.value = -speed

    def reverse(self):
        self.value *= -1

    def stop(self):
        self._motor.stop()
        self._throttle = 0

    @property
    def value(self) -> float:
        return self._throttle

    @value.setter
    def value(self, value: float):
        self._throttle = max(-1, min(1, value))
        if value != 0:
            self._motor.speed(self._throttle*100)
        else:
            self._motor.stop()

    @property
    def is_active(self) -> bool:
        return self._throttle != 0


class ExplorerHatService:
    def __init__(self) -> None:
        self.left_motor = Motor(explorerhat.motor.one)
        self.right_motor = Motor(explorerhat.motor.two)
        self.last_contact = 0
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("motors/#")
    
    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        print(msg.topic+" "+str(payload))
        motor_handlers = {
            "motors/forward": self.forward,
            "motors/backward": self.backward,
            "motors/left": self.left,
            "motors/right": self.right,
            "motors/stop": self.stop,
            "motors/reverse": self.reverse,
            "motors/values": self.set_values
        }
        if msg.topic in motor_handlers:
            motor_handlers[msg.topic](payload)
        self.last_contact = time.monotonic()

    def forward(self, payload: dict):
        speed = payload.get("speed", 1)
        curve = payload.get("curve", 0)
        self.left_motor.forward(speed - curve)
        self.right_motor.forward(speed + curve)

    def backward(self, payload: dict):
        speed = payload.get("speed", 1)
        curve = payload.get("curve", 0)
        self.left_motor.backward(speed + curve)
        self.right_motor.backward(speed - curve)

    def left(self, payload: dict):
        speed = payload.get("speed", 1)
        self.left_motor.backward(speed)
        self.right_motor.forward(speed)
    
    def right(self, payload: dict):
        speed = payload.get("speed", 1)
        self.left_motor.forward(speed)
        self.right_motor.backward(speed)
    
    def reverse(self, payload: dict):
        self.left_motor.value *= -1
        self.right_motor.value *= -1
    
    def stop(self, payload: dict = None):
        self.left_motor.stop()
        self.right_motor.stop()

    def get_values(self):
        return (self.left_motor.value, self.right_motor.value)
    
    def set_values(self, payload: dict):
        self.left_motor.value = payload["left"]
        self.right_motor.value = payload["right"]


service = ExplorerHatService()
service_name = "ExplorerHat"
username, password = "robot", "robot"
host, port = "localhost", 9001
client = mqtt.Client(client_id=f"{service_name}_{randint(0, 1000)}", transport="websockets")

client.username_pw_set(username, password)

print("Connecting")
client.on_connect = service.on_connect
client.on_message = service.on_message
client.connect(host, port)

while True:
    client.loop()
    if time.monotonic() > service.last_contact + 1:
        service.stop()

