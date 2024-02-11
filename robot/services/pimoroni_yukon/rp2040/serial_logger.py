import sys
import json
import time
import uasyncio as asyncio

from pimoroni_yukon import Yukon


def mqtt_output(topic, message):
    print(f"mqtt_output##{topic}:{message}")

class AsyncLedFlasher:
    async def run(self):
        # Setup the yukon
        yukon = Yukon()
        try:
            yukon.enable_main_output()
            print("Starting main motor loop")
            # Service the stream
            while True:
                yukon.set_led('A', True)
                yukon.set_led('B', False)
                await asyncio.sleep(0.5)
                yukon.monitor_once()
                yukon.set_led('A', False)
                yukon.set_led('B', True)
                await asyncio.sleep(0.5)
                yukon.monitor_once()
        finally:
            # Put the board back into a safe state, regardless of how the program may have ended
            yukon.reset()


async def main():
    # Stream reader
    input_stream = asyncio.StreamReader(sys.stdin)
    print("Starting serial handling loop")
    while True:
        print("Running readline")
        line = await input_stream.readline()
        line = line.decode().strip()
        print(f"Received message at Yukon: {line}")
        try:
            topic, payload = line.split(":", 1)
            payload = json.loads(payload)
        except ValueError as err:
            print(f"Invalid message received to Yukon: {line}, {err}")
            continue
        print(f"Topic is: {topic}")
        print(f"Payload is: {payload}")

asyncio.run(main())
