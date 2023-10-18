import DFRobot_RaspberryPi_Expansion_Board
import gpiozero


class Motor(gpiozero.Device):
    def __init__(self, board :DFRobot_RaspberryPi_Expansion_Board.DFRobot_Expansion_Board_IIC, 
                 pwm_chan: int, phase: int):
        self.board = board
        self.pwm_chan = pwm_chan
        self.phase = gpiozero.DigitalOutputDevice(phase)
        self._throttle = 0
        
    def forward(self, speed: float=1):
        self.value = speed

    def backward(self, speed: float=1):
        self.value = -speed

    def reverse(self):
        self.value *= -1

    def stop(self):
        self.value = 0

    @property
    def value(self) -> float:
        return self._throttle

    @value.setter
    def value(self, value: float):
        self._throttle = value
        if value > 0:
            self.phase.off()
            self.board.set_pwm_duty(self.pwm_chan, value * 100.0)
        elif value < 0:
            self.phase.on()
            self.board.set_pwm_duty(self.pwm_chan, 100 - value * 100.0)
        else:
            self.board.set_pwm_duty(self.pwm_chan, 0)
            self.phase.off()

    @property
    def is_active(self) -> bool:
        return self._throttle != 0


class Robot:
    def __init__(self) -> None:
        self.board = DFRobot_RaspberryPi_Expansion_Board.DFRobot_Expansion_Board_IIC(1, 0x10)
        self.board.begin()
        self.board.set_pwm_enable()
        self.board.set_pwm_frequency(1000)
        self.left_motor = Motor(self.board, 0, 0)
        self.right_motor = Motor(self.board, 1, 1)
    
    def forward(self, speed=1, curve_left=0, curve_right=0):
        self.left_motor.forward(speed - curve_left)
        self.right_motor.forward(speed - curve_right)

    def backwards(self, speed=1, curve_left=0, curve_right=0):
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
