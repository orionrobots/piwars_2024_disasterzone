import sys
import json
import time
import uasyncio as asyncio

from pimoroni_yukon import Yukon, SLOT1, SLOT2, SLOT3, SLOT4, SLOT5, SLOT6
from pimoroni_yukon.modules import BigMotorModule
from pimoroni_yukon.timing import ticks_ms, ticks_add

GEAR_RATIO = 30                         # The gear ratio of the motor
ENCODER_CPR = 12                        # The number of counts a single encoder shaft revolution will produce
MOTOR_CPR = GEAR_RATIO * ENCODER_CPR    # The number of counts a single motor shaft revolution will produce

def mqtt_output(topic, message):
    print(f"mqtt_output##{topic}:{message}")

def log(message):
    mqtt_output('log/yukon', f'"{message}"')

class YukonManager:
    last_contact = time.ticks_ms()
    async def run(self):
        # Setup the yukon
        yukon = Yukon() 
        left_motor_module  = BigMotorModule(encoder_pio=0,    # Create a BigMotorModule object, with details of the encoder
                                    encoder_sm=0,
                                    counts_per_rev=MOTOR_CPR)
        right_motor_module = BigMotorModule(encoder_pio=0,    # Create a BigMotorModule object, with details of the encoder
                                    encoder_sm=1,
                                    counts_per_rev=MOTOR_CPR)
        try:
            yukon.register_with_slot(left_motor_module, SLOT3)
            yukon.register_with_slot(right_motor_module, SLOT2) 
            yukon.verify_and_initialise()
            yukon.enable_main_output()
            # Enable the modules
            left_motor_module.enable()
            right_motor_module.enable()
            log("Getting motors")
            self.left_motor = left_motor_module.motor
            self.right_motor = right_motor_module.motor
            log("Starting main motor loop")
            # Service the stream
            while True:
                asyncio.sleep(0.1)
                yukon.monitored_sleep_ms(10)
                if self.last_contact != 0 and time.ticks_diff(time.ticks_ms(), self.last_contact) > 1000:
                    self.last_contact = 0
                    self.left_motor.stop(0)
                    self.right_motor.stop(0)
        finally:
            # Put the board back into a safe state, regardless of how the program may have ended
            yukon.reset()

    def turn_left(self, speed):
        self.left_motor.enable()
        self.left_motor.speed(-speed)
        self.right_motor.enable()
        self.right_motor.speed(speed)
        self.last_contact = time.ticks_ms()
    
    def turn_right(self, speed):
        self.right_motor.enable()
        self.right_motor.speed(-speed)
        self.left_motor.enable()
        self.left_motor.speed(speed)
        self.last_contact = time.ticks_ms()

    def forward(self, speed, curve):
        self.left_motor.enable()
        self.right_motor.enable()
        self.left_motor.speed(speed - curve)
        self.right_motor.speed(speed + curve)
        self.last_contact = time.ticks_ms()

    def backward(self, speed, curve):
        self.left_motor.enable()
        self.right_motor.enable()
        self.left_motor.speed(speed - curve)
        self.right_motor.speed(speed + curve)
        self.last_contact = time.ticks_ms()

    def set_values(self, left, right):
        self.left_motor.enable()
        self.right_motor.enable()
        self.left_motor.speed(left)
        self.right_motor.speed(right)
        self.last_contact = time.ticks_ms()

    def stop(self):
        self.left_motor.stop(0)
        self.right_motor.stop(0)
        self.last_contact = time.ticks_ms()


async def main():
    # Stream reader
    input_stream = asyncio.StreamReader(sys.stdin)
    yukon_manager = YukonManager()
    asyncio.create_task(yukon_manager.run())
    while True:
        line = await input_stream.readline()
        if line is None:
            break
        line = line.decode().strip()
        topic, payload = line.split(":", 1)
        try:
            payload = json.loads(payload)
        except ValueError:
            log(f"Invalid JSON received to Yukon: {line}")
            continue
        log(f"Received message at Yukon: {line}")        
        if topic == "motors/left":
            yukon_manager.turn_left(payload)
        elif topic == "motors/right":
            yukon_manager.turn_right(payload)
        elif topic == "motors/stop":
            yukon_manager.stop()
        elif topic == "motors/forward":
            yukon_manager.forward(payload.get("speed", 1), payload.get("curve", 0))
        elif topic == "motors/backward":
            yukon_manager.backward(payload.get("speed", 1), payload.get("curve", 0))
        elif topic == "motors/set_values":
            yukon_manager.set_values(payload["left"], payload["right"])

asyncio.run(main())
