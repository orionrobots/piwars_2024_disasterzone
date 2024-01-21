import time

from typing import Optional

from paho.mqtt.client import MQTTMessage, Client
import serial
import serial.threaded

from robot.common import service_base
from robot.common.settings import RobotSettings

class SerialToMqtt(serial.threaded.LineReader):
    newline = b"\n"
    def __init__(self):
        self._buffer = bytearray()
        self.client: Optional[Client] = None

    def __call__(self):
        return self

    def handle_line(self, line: str):
        """Lines of the format topic:payload - ie yukon/status:"ready" 
        """
        print(f"Received message from Yukon: {line}")
        topic, payload = line.split(":", 1)
        if self.client is not None:
            self.client.publish(topic, payload)


class YukonService(service_base.ServiceBase):
    name = "yukon"
    def __init__(self, settings: RobotSettings) -> None:
        super().__init__(settings)
        self.board = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)
        # Start listening to the serial port
        self.serial_worker = SerialToMqtt()
        self.serial_thread = serial.threaded.ReaderThread(self.board, self.serial_worker)
        self.serial_worker.start()

    def on_connect(self, client: Client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        print("Subscribing")
        client.subscribe("motors/#")
        client.message_callback_add("motors/#", self.send_motor_message_to_yukon)
        self.serial_worker.client = client

    def send_motor_message_to_yukon(self, client: Client, userdata, msg: MQTTMessage):
        print(f"Sending message to Yukon: {msg.topic} {msg.payload}")
        self.serial_worker.write_line(f"{msg.topic}:{msg.payload}")

service = YukonService()
client = service_base.connect(service)

while True:
    client.loop()
