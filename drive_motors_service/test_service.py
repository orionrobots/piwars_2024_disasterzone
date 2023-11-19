import paho.mqtt.client as mqtt

from robot_settings import Settings

settings = Settings()
print("Creating client")
client = mqtt.Client(client_id="drive_motors",
                     transport="websockets",
                     protocol=mqtt.MQTTv31)
print("Setting username")
client.username_pw_set(username=settings.mqtt_username, password=settings.mqtt_password)
# print("Setting TLS")
# client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED)
print("Connecting")
client.connect(settings.mqtt_host, settings.mqtt_port)

client.publish("drive_motors/test", "hello world")
print("Starting loop")
client.loop_forever()
