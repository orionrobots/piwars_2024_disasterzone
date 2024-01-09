from typing import Optional

from paho.mqtt.client import MQTTMessage, Client
import serial
import serial.threaded

from robot.common.service_base import ServiceBase
from robot.common.settings import RobotSettings


class SerialToMqtt(serial.threaded.Protocol):
    newline = b"\n"
    def __init__(self):
        self._buffer = bytearray()
        self.client: Optional[Client] = None

    def __call__(self):
        return self

    def data_received(self, data: bytes):
        self._buffer.extend(data)
        while self.newline in self._buffer:
            message = self._buffer.split(self.newline)[0]
            self._buffer = self._buffer.split(self.newline)[1:]
            topic, payload = message.split(b":", 1)
            print(f"Received message from yukon: {topic} {payload}")
            if self.client is not None:
                self.client.publish(topic.decode(), payload.decode())

class YukonService(ServiceBase):
    service_name = "yukon"

    def __init__(self, settings: RobotSettings) -> None:
        super().__init__(settings)
        self.board = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)
        self.serial_worker = SerialToMqtt()
        self.serial_thread = serial.threaded.ReaderThread(self.board, self.serial_worker)
        self.serial_worker.start()
    
    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        print("Subscribing")
        client.subscribe("motors/#")
        client.message_callback_add("motors/#", self.send_motor_message_to_yukon)
        self.serial_worker.client = client

    def send_message_to_yukon(self, client: Client, userdata, msg: MQTTMessage):
        print(f"Sending message to yukon: {msg.topic} {msg.payload}")
        self.board.write(f"{msg.topic}:{msg.payload}\n".encode())
