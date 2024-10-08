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
    board: serial.Serial

    def __init__(self, settings: RobotSettings) -> None:
        super().__init__()
        print("Opening serial port")

        devices_to_try = ["/dev/ttyACM0", "/dev/ttyACM1"]
        for device in devices_to_try:
            try:
                self.board = serial.Serial(device, 115200, timeout=0.1)
                break
            except serial.SerialException as e:
                print(f"Failed to open {device}: {e}")
                continue
        if not self.board:
            raise serial.SerialException(f"Failed to open any of {devices_to_try}")

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
        client.subscribe("leds/#")
        client.subscribe("all/#")
        client.subscribe("servos/#")
        client.subscribe("dual_motors/#")
        client.subscribe("line_follower/control")
        client.message_callback_add("motors/#", self.send_message_to_yukon)
        client.message_callback_add("leds/#", self.send_message_to_yukon)
        client.message_callback_add("all/#", self.send_message_to_yukon)
        client.message_callback_add("servos/#", self.send_message_to_yukon)
        client.message_callback_add("dual_motors/#", self.send_message_to_yukon)
        client.message_callback_add("line_follower/control", self.send_message_to_yukon)
        print("Callbacks added")
        self.serial_worker.mqtt_client = client

    def send_message_to_yukon(self, client: Client, userdata, msg: MQTTMessage):
        serial_message=f"{msg.topic}:{msg.payload.decode()}"
        print(f"Sending message to Yukon: {serial_message}")
        self.serial_worker.write_line(f"{serial_message}")

print("Creating service")
service = YukonService(RobotSettings())
print("Connecting")
client = service_base.connect(service)
print("Connected. Starting loop")
client.loop_forever()
