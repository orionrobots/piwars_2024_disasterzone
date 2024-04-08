from approxeng.input.selectbinder import ControllerResource
from time import sleep

while True:
    try:
        with ControllerResource() as joystick:
            print('Found a joystick and connected')
            while joystick.connected:
                # This is where you'd normally do stuff with the joystick
                # buttons, axes, etc
                print("Left:", joystick.lx, joystick.ly)
                print("Lt2:", joystick.l2)
                print("Right:", joystick.rx, joystick.ry)
                print("Rt2:", joystick.r2)
                # L2 and r2 generated presses as well as pressure. I probably only mean presses for now.
                print("Buttons:", joystick.check_presses())
                sleep(0.1)
    except IOError:
        # No joystick found, wait for a bit before trying again
        print('Unable to find any joysticks')
        sleep(1.0)
