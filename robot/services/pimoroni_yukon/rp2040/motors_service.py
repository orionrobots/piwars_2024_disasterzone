import sys
import json
import time
import uasyncio as asyncio

from pimoroni_yukon import Yukon, SLOT1, SLOT2, SLOT3, SLOT4, SLOT5, SLOT6
from pimoroni_yukon.modules import BigMotorModule
from pimoroni import REVERSED_DIR

GEAR_RATIO = 30                         # The gear ratio of the motor
ENCODER_CPR = 12                        # The number of counts a single encoder shaft revolution will produce
MOTOR_CPR = GEAR_RATIO * ENCODER_CPR    # The number of counts a single motor shaft revolution will produce

def mqtt_output(topic, message):
    print(f"mqtt_output##{topic}:{message}")

class YukonManager:
    last_contact = 0
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
            yukon.register_with_slot(right_motor_module, SLOT3)
            yukon.register_with_slot(left_motor_module, SLOT2) 
            yukon.verify_and_initialise()
            yukon.enable_main_output()
            # Enable the modules
            left_motor_module.enable()
            right_motor_module.enable()
            print("Getting motors")
            self.left_motor = left_motor_module.motor
            self.right_motor = right_motor_module.motor
            self.left_motor.direction(REVERSED_DIR)
            self.right_motor.direction(REVERSED_DIR)
            print("Starting main motor loop")
            # Service the stream
            while True:
                await asyncio.sleep(0.1)
                yukon.monitor_once()
                if self.last_contact != 0 and time.ticks_diff(time.ticks_ms(), self.last_contact) > 1000:
                    self.last_contact = 0
                    print("No contact from mqtt, stopping")
                    self.stop()
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
        print("Driving forward")
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
        self.left_motor.stop()
        self.right_motor.stop()


async def main():
    # Stream reader
    input_stream = asyncio.StreamReader(sys.stdin)
    yukon_manager = YukonManager()
    asyncio.create_task(yukon_manager.run())
    print("Starting serial handling loop")
    while True:
        line = await input_stream.readline()
        line = line.decode().strip()
        print(f"Received message at Yukon: {line}")
        try:
            topic, payload = line.split(":", 1)
            payload = json.loads(payload)
        except ValueError as err:
            print(f"Invalid message received at Yukon: {line}, {err}")
            continue
        try:
            if topic == "motors/left":
                yukon_manager.turn_left(payload)
            elif topic == "motors/right":
                yukon_manager.turn_right(payload)
            elif topic == "motors/stop" or topic == "all/stop":
                yukon_manager.stop()
            elif topic == "motors/forward":
                yukon_manager.forward(payload.get("speed", 1), payload.get("curve", 0))
            elif topic == "motors/backward":
                yukon_manager.backward(payload.get("speed", 1), payload.get("curve", 0))
            elif topic == "motors/set_values":
                yukon_manager.set_values(payload.get("left", 0), payload.get("right",0))
            else:
                print(f"Invalid message received at Yukon: {line}")
        except (KeyError, AttributeError) as err:
            print(f"Invalid message received at Yukon: {line}, {err}")

asyncio.run(main())
