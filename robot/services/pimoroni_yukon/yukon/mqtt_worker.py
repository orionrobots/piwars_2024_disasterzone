import sys
import json

from pimoroni_yukon import Yukon, SLOT1, SLOT2, SLOT3, SLOT4, SLOT5, SLOT6
from pimoroni_yukon.modules import BigMotorModule
from pimoroni_yukon.timing import ticks_ms, ticks_add

import uasyncio as asyncio

GEAR_RATIO = 30                         # The gear ratio of the motor
ENCODER_CPR = 12                        # The number of counts a single encoder shaft revolution will produce
MOTOR_CPR = GEAR_RATIO * ENCODER_CPR    # The number of counts a single motor shaft revolution will produce


def log(message):
    print(f"log/yukon: {message}")


class YukonManager:
    async def run(self):
        # Setup the yukon
        yukon = Yukon() 
        left_motor_module  = BigMotorModule(encoder_pio=0,    # Create a BigMotorModule object, with details of the encoder
                                    encoder_sm=0,
                                    counts_per_rev=MOTOR_CPR)
        right_motor_module = BigMotorModule(encoder_pio=0,    # Create a BigMotorModule object, with details of the encoder
                                    encoder_sm=1,
                                    counts_per_rev=MOTOR_CPR)
        self.left_motor = left_motor_module.motor
        self.right_motor = right_motor_module.motor
        try:
            yukon.register_with_slot(left_motor_module, SLOT3)
            yukon.register_with_slot(right_motor_module, SLOT2) 
            yukon.verify_and_initialise()
            yukon.enable_main_output()
            # Enable the modules
            left_motor_module.enable()
            right_motor_module.enable()
            # Service the stream
            while True:
                asyncio.sleep(0.1)
                yukon.monitored_sleep_ms(10)
        finally:
            # Put the board back into a safe state, regardless of how the program may have ended
            yukon.reset()


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
        payload = json.loads(payload)
        if topic == "motors/left":
            log(f"motors/left: {payload}")
            yukon_manager.left_motor.enable()
            yukon_manager.left_motor.speed(payload)
            yukon_manager.right_motor.enable()
            yukon_manager.right_motor.speed(-payload)
        elif topic == "motors/right":
            log(f"motors/right: {payload}")
            yukon_manager.right_motor.enable()
            yukon_manager.right_motor.speed(payload)
            yukon_manager.left_motor.enable()
            yukon_manager.left_motor.speed(-payload)
        elif topic == "motors/stop":
            log("motors/stop")
            yukon_manager.left_motor.stop(0)
            yukon_manager.right_motor.stop(0)
        elif topic == "motors/forward":
            speed = payload.get("speed", 1)
            curve = payload.get("curve", 0)
            log(f"motors/forward: {payload}")
            yukon_manager.left_motor.enable()
            yukon_manager.right_motor.enable()
            yukon_manager.left_motor.speed(speed - curve)
            yukon_manager.right_motor.speed(speed + curve)
        elif topic == "motors/backward":
            speed = payload.get("speed", 1)
            curve = payload.get("curve", 0)
            log(f"motors/backward: {payload}")
            yukon_manager.left_motor.enable()
            yukon_manager.right_motor.enable()
            yukon_manager.left_motor.speed(speed - curve)
            yukon_manager.right_motor.speed(speed + curve)
        elif topic == "motors/set_values":
            log(f"motors/set_values: {payload}")
            yukon_manager.left_motor.enable()
            yukon_manager.right_motor.enable()
            yukon_manager.left_motor.speed(payload["left"])
            yukon_manager.right_motor.speed(payload["right"])
        
