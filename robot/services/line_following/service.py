from paho.mqtt.client import MQTTMessage, Client

from robot.common import service_base
from robot.common.settings import RobotSettings


class LineFollowerService(service_base.ServiceBase):
    name = "line_following"

    def __init__(self, settings: RobotSettings) -> None:
        self.running = False
        super().__init__()

    def run(self):
        pass
