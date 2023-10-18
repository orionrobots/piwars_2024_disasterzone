from adafruit_crickit import crickit


class Robot:
    def __init__(self) -> None:
        self.left_motor = crickit.dc_motor_1
        self.right_motor = crickit.dc_motor_2
    
    def backward(self, speed=1, curve_left=0, curve_right=0):
        self.left_motor.throttle = -speed + curve_left
        self.right_motor.throttle = -speed + curve_right
    
    def forward(self, speed=1, curve_left=0, curve_right=0):
        self.left_motor.throttle = speed - curve_left
        self.right_motor.throttle = speed - curve_right

    def left(self, speed=1):
        self.left_motor.throttle = -speed
        self.right_motor.throttle = speed
    
    def right(self, speed=1):
        self.left_motor.throttle = speed
        self.right_motor.throttle = -speed
    
    def reverse(self):
        self.left_motor.throttle *= -1
        self.right_motor.throttle *= -1
    
    def stop(self):
        self.left_motor.throttle = 0
        self.right_motor.throttle = 0

    @property
    def value(self):
        return (self.left_motor.throttle, self.right_motor.throttle)
    
    @value.setter
    def value(self, values:tuple):
        self.left_motor.throttle = values[0]
        self.right_motor.throttle = values[1]

