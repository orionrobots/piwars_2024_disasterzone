import paho.mqtt.client as mqtt
from random import randint
from robot.common.settings import RobotSettings


class ServiceBase:
    name = "base"
    
    def on_connect(self, client, userdata, flags, rc):
        """Override, make subscriptions here"""
        print("Connected with result code "+str(rc))
    
    def on_message(self, client, userdata, msg):
        """Handle messages here"""
        print(msg.topic+" "+str(msg.payload))


def connect(service: ServiceBase) -> mqtt.Client:
    """Get the service connected, and return the new client"""
    settings = RobotSettings()
    host, port = "localhost", settings.mqtt_port
    client = mqtt.Client(client_id=f"{service.name}_{randint(0, 1000)}", transport="websockets")
    client.will_set("all/stop", 0)
    client.username_pw_set(settings.mqtt_username, settings.mqtt_password.get_secret_value())

    print("Connecting")
    client.on_connect = service.on_connect
    client.on_message = service.on_message
    client.connect(host, port)
    return client
