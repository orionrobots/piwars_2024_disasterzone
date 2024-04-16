import subprocess
import json
from paho.mqtt.client import MQTTMessage, Client


from robot.common import service_base
from robot.common.settings import RobotSettings

class LauncherService(service_base.ServiceBase):
    name = "launcher"

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        client.subscribe("launcher/#")
        client.message_callback_add("launcher/start", self.start_systemd_unit)
        client.message_callback_add("launcher/stop", self.stop_systemd_unit)
        client.message_callback_add("launcher/restart", self.restart_systemd_unit)
        client.message_callback_add("launcher/poweroff", self.poweroff)

    def start_systemd_unit(self, client: Client, userdata, msg: MQTTMessage):
        unit_name = json.loads(msg.payload)
        subprocess.run(["systemctl", "start", unit_name])
        print(unit_name, "started")

    def stop_systemd_unit(self, client: Client, userdata, msg: MQTTMessage):
        unit_name = json.loads(msg.payload)
        subprocess.run(["systemctl", "stop", unit_name])
        print(unit_name, "stopped")

    def restart_systemd_unit(self, client: Client, userdata, msg: MQTTMessage):
        unit_name = json.loads(msg.payload)
        subprocess.run(["systemctl", "restart", unit_name])
        print(unit_name, "restarted")

    def poweroff(self, client: Client, userdata, msg: MQTTMessage):
        print("Powering off")
        subprocess.run(["poweroff"])

print("Creating Launcher service")
service = LauncherService()
print("Connecting")
client = service_base.connect(service)
print("Connected. Starting loop")
client.loop_forever()
