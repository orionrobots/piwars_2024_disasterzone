from typing import Optional

from paho.mqtt.client import MQTTMessage, Client
import serial
import serial.threaded

from robot.common import service_base
from robot.common.settings import RobotSettings

class SerialToMqtt(serial.threaded.LineReader):
    def __init__(self):
        super().__init__()
        self.mqtt_client: Optional[Client] = None
        print("SerialToMqtt members:", dir(self))

    def __call__(self):
        return self

    def log(self, msg):
        print(msg)
        if self.mqtt_client:
            self.mqtt_client.publish("log/yukon_service", msg)

    def handle_line(self, line: str):
        """Lines of the format topic:payload - ie yukon/status:"ready" 
        Start with mqtt_output## to send to mqtt
        """
        if not line.startswith("mqtt_output##"):
            self.log(f"Yukon: {line}")
            return
        elif ":" not in line:
            self.log(f"Invalid message received from Yukon: {line}")
        topic, payload = line.split("##")[1].split(":", 1)
        if self.mqtt_client is not None:
            self.mqtt_client.publish(topic, payload)

    def connection_lost(self, exc):
        if exc:
            print(f"Serial connection error: {exc}")


class YukonService(service_base.ServiceBase):
    name = "yukon"
    def __init__(self, settings: RobotSettings) -> None:
        super().__init__()
        print("Opening serial port")
        self.board = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)
        # Start listening to the serial port
        print("Starting serial thread")
        self.serial_worker = SerialToMqtt()
        self.serial_thread = serial.threaded.ReaderThread(self.board, self.serial_worker)
        self.serial_thread.start()
        print("Serial thread started")

    def on_connect(self, client: Client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        print("Subscribing")
        client.subscribe("motors/#")
        client.message_callback_add("motors/#", self.send_motor_message_to_yukon)
        print("Callbacks added")
        self.serial_worker.mqtt_client = client

    def send_motor_message_to_yukon(self, client: Client, userdata, msg: MQTTMessage):
        serial_message=f"{msg.topic}:{msg.payload.decode()}"
        print(f"Sending message to Yukon: {serial_message}")
        self.serial_worker.write_line(f"{serial_message}")

print("Creating service")
service = YukonService(RobotSettings())
print("Connecting")
client = service_base.connect(service)
print("Connected. Starting loop")
client.loop_forever()
