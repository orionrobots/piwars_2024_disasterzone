import inventorhatmini
import gpiozero


class Motor(gpiozero.Device):
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
        self._throttle = value
        if value != 0:
            self._motor.enable()
            self._motor.speed(value)
        else:
            self._motor.stop()

    @property
    def is_active(self) -> bool:
        return self._throttle != 0


class Robot:
    def __init__(self) -> None:
        self.board = inventorhatmini.InventorHATMini()
        self.left_motor = Motor(self.board.motors[1])
        self.right_motor = Motor(self.board.motors[0])

    def forward(self, speed=1, curve_left=0, curve_right=0):
        self.left_motor.forward(speed - curve_left)
        self.right_motor.forward(speed - curve_right)

    def backward(self, speed=1, curve_left=0, curve_right=0):
        self.left_motor.backward(speed + curve_left)
        self.right_motor.backward(speed + curve_right)

    def left(self, speed=1):
        self.left_motor.backward(speed)
        self.right_motor.forward(speed)
    
    def right(self, speed=1):
        self.left_motor.forward(speed)
        self.right_motor.backward(speed)
    
    def reverse(self):
        self.left_motor.value *= -1
        self.right_motor.value *= -1
    
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    @property
    def value(self):
        return (self.left_motor.value, self.right_motor.value)
    
    @value.setter
    def value(self, values:tuple):
        self.left_motor.value = values[0]
        self.right_motor.value = values[1]
