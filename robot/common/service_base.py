import json
from random import randint
import time
from typing import Callable

import paho.mqtt.client as mqtt

from robot.common.settings import RobotSettings

class ServiceBase:
    last_contact = 0
    service_name = "unnamed_service"
    host = "localhost"

    def __init__(self, settings: RobotSettings) -> None:
        self.settings = settings

    def connect(self):
        self.client = mqtt.Client(client_id=f"{self.service_name}_{randint(0, 1000)}", transport="websockets")

        self.client.username_pw_set(self.settings.mqtt_username, self.settings.mqtt_password.get_secret_value())

        print("Connecting")
        self.client.on_connect = self.on_connect
        self.client.connect(self.host, self.settings.mqtt_port)
    
    def loop_forever(self):
        while True:
            self.client.loop()
            if time.monotonic() > self.last_contact + 1:
                self.stop()

    def print_message(self, client, userdata, msg):
        print(f"Print message: {msg.topic} {msg.payload}")

    def message_callback_add(self, topic: str, callback: Callable):
        def __inner(client, userdata, msg):
            payload = json.loads(msg.payload)
            callback(payload)
            self.last_contact = time.monotonic()

        self.client.message_callback_add(topic, __inner)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def stop(self):
        pass
