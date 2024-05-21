import json
import time

from paho.mqtt.client import MQTTMessage, Client
import numpy as np

from robot.common import service_base
from robot.common.pid_control import PIController


class LineFollowingService(service_base.ServiceBase):
    name = "line_following"
    THRESHOLD = 105
    EXPECTED = 1.5
    SPEED = 0.5

    def __init__(self) -> None:
        self.pid = PIController(-0.8, 0)
        self.last_time = time.time()
        super().__init__()

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        client.subscribe("line_follower/#")
        client.subscribe("all/stop")
        client.message_callback_add("line_follower/differences", self.handle_data)
        client.message_callback_add("all/stop", self.stop)
        self.publish_json("line_follower/control", {"enabled": True})

    def handle_data(self, client: Client, userdata, msg: MQTTMessage):
        # sense
        differences = np.array(json.loads(msg.payload))
        print("Differences", differences)
        indexes = np.where(differences > self.THRESHOLD)[0]
        print("Indexes", indexes)
        if indexes.size == 0:
            return
        actual = np.average(indexes)
        # think
        error = actual - self.EXPECTED
        dt = max(time.time() - self.last_time, 0.01)
        self.last_time = time.time()
        print("actual", actual, "error", error, "dt", dt)
        control = np.clip(self.pid.control(error, dt), -1, 1)
        # act
        self.publish_json("motors/forward", {"speed": self.SPEED, "curve": control})

    def stop(self, client: Client, userdata, msg: MQTTMessage):
        self.publish_json("line_follower/control", {"enabled": False})

print("Creating Line Following service")
service = LineFollowingService()
print("Connecting")
client = service_base.connect(service)
print("Connected. Starting loop")
client.loop_forever()
