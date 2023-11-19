# import ssl
import paho.mqtt.client as mqtt
from random import randint

from robot.robot_settings import Settings


class BaseService:
    port = 9001

    def __init__(self, service_name):
        self.settings: Settings = Settings()
        self.client: mqtt.Client = None
        self.service_name = service_name

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("demo/#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def run(self):
        print("Creating client")
        self.client = mqtt.Client(client_id=f"{self.service_name}_{randint(0, 1000)}",
                             transport="websockets")
        print("Setting username")
        self.client.username_pw_set(
            self.settings.mqtt_username, 
            password=self.settings.mqtt_password)
        
        host = self.settings.mqtt_host

        # print("Setting TLS")
        # self.client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED)

        print("Setting callbacks")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        print("Connecting")
        self.client.connect(host, self.port)

        print("Ready to loop")
        # We could add a background task runner here (on loop or something)
