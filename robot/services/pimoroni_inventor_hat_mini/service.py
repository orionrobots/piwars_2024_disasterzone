import inventorhatmini

from robot.common.service_base import ServiceBase
from robot.common.settings import RobotSettings


def limit(value: float, min_value: float, max_value: float) -> float:
    return min(max(value, min_value), max_value)

class Motor:
    def __init__(self, board_motor :inventorhatmini.Motor):
        self._motor = board_motor
        self._throttle = 0
        
    def forward(self, speed: float=1):
        self.value = speed

    def backward(self, speed: float=1):
        self.value = -speed

    def reverse(self):
        self.value *= -1

    def stop(self):
        self._motor.stop()
        self._throttle = 0

    @property
    def value(self) -> float:
        return self._throttle

    @value.setter
    def value(self, value: float):
        self._throttle = limit(value, -1, 1)
        if value != 0:
            self._motor.enable()
            self._motor.speed(self._throttle)
        else:
            self._motor.stop()

    @property
    def is_active(self) -> bool:
        return self._throttle != 0


class InventorHatService(ServiceBase):
    service_name = "inventorhat"
    def __init__(self, settings: RobotSettings) -> None:
        super().__init__(settings)
        self.board = inventorhatmini.InventorHATMini()
        self.left_motor = Motor(self.board.motors[1])
        self.right_motor = Motor(self.board.motors[0])

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        print("Subscribing")
        client.subscribe("motors/#")
        self.message_callback_add("motors/forward", self.forward)
        self.message_callback_add("motors/backward", self.backward)
        self.message_callback_add("motors/left", self.left)
        self.message_callback_add("motors/right", self.right)
        self.message_callback_add("motors/stop", self.stop)
        self.message_callback_add("motors/reverse", self.reverse)
        self.message_callback_add("motors/values", self.set_values)
        self.client.message_callback_add("motors/#", self.print_message)
        print("Callbacks ready")

    def forward(self, payload: dict):
        speed = payload.get("speed", 1)
        curve = payload.get("curve", 0)

        self.left_motor.forward(speed - curve)
        self.right_motor.forward(speed + curve)

    def backward(self, payload: dict):
        speed = payload.get("speed", 1)
        curve = payload.get("curve", 0)

        self.left_motor.backward(speed - curve)
        self.right_motor.backward(speed + curve)

    def left(self, payload: dict):
        speed = payload.get("speed", 1)
        self.left_motor.backward(speed)
        self.right_motor.forward(speed)

    def right(self, payload: dict):
        speed = payload.get("speed", 1)
        self.left_motor.forward(speed)
        self.right_motor.backward(speed)

    def reverse(self, payload: dict = None):
        self.left_motor.value *= -1
        self.right_motor.value *= -1

    def stop(self, payload: dict = None):
        self.left_motor.stop()
        self.right_motor.stop()

    def get_values(self):
        return (self.left_motor.value, self.right_motor.value)

    def set_values(self, payload: dict):
        self.left_motor.value = payload["left"]
        self.right_motor.value = payload["right"]

print("Starting service")
settings = RobotSettings()
service = InventorHatService(settings)
service.connect()
print("Looping")
service.loop_forever()
