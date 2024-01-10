"""Test code for Yukon board.
Flash the LED's in sequence.
Derivative of https://github.com/pimoroni/yukon/blob/main/examples/board/blink_led.py
Press "Boot/User" to exit the program.
"""
from pimoroni_yukon import Yukon

# Constants
SLEEP = 0.10    # The time to sleep between each toggle

# Variables
yukon = Yukon()     # A new Yukon object
led_state = False

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    # Loop until the BOOT/USER button is pressed
    while not yukon.is_boot_pressed():

        led_state = not led_state           # Toggle the LED state
        yukon.set_led('A', led_state)       # Set the LED to the new state
        yukon.set_led('B', not led_state)   # Set the other LED to the opposite state

        yukon.monitored_sleep(SLEEP)                   # Sleep for a number of seconds
        yukon.print_readings()
finally:
    # Put the board back into a safe state, regardless of how the program may have ended
    yukon.reset()
