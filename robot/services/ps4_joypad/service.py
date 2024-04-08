from time import sleep

from approxeng.input.selectbinder import ControllerResource
from paho.mqtt.client import MQTTMessage, Client

from robot.common import service_base
from robot.common.settings import RobotSettings


class PS4ControllerService(service_base.ServiceBase):
    name = "ps4_joypad"

    def __init__(self, settings: RobotSettings) -> None:
        super().__init__()

    def run(self):
        motors_centered = False
        servo_centered = False
        while True:
            try:
                with ControllerResource() as joystick:
                    self.publish_json("joypad/connected", 1)
                    print('Found a joystick and connected')
                    while joystick.connected:
                        # Direct motors
                        if joystick.ly == 0 and joystick.lx == 0 and not motors_centered:
                            motors_centered = True
                            self.publish_json("motors/stop", {})
                        elif joystick.ly != 0 or joystick.lx != 0:
                            self.publish_json("motors/forward", {"speed": joystick.ly, "curve": -joystick.lx})
                            motors_centered = False
                        # Servos
                        if joystick.rx == 0 and joystick.ry == 0 and not servo_centered:
                            servo_centered = True
                            self.publish_json("servos/set", {"index": 0, "position": 0})
                            self.publish_json("servos/set", {"index": 1, "position": 0})
                        elif joystick.rx != 0 or joystick.ry != 0:
                            self.publish_json("servos/set", {"index": 0, "position": joystick.rx * -30})
                            self.publish_json("servos/set", {"index": 1, "position": joystick.ry * 30})
                            servo_centered = False
                        joystick.check_presses()
                        if "l2" in joystick.presses:
                            self.publish_json("servos/set", {"index": 2, "position": -50})
                        elif "l2" in joystick.releases:
                            self.publish_json("servos/set", {"index": 2, "position": 0})
                        if "r2" in joystick.presses:
                            self.publish_json("rollers/start", {})
                        elif "r2" in joystick.releases:
                            self.publish_json("rollers/stop", {})
                        if "triangle" in joystick.presses:
                            self.publish_json("all/stop", {})
                        sleep(1/50)
            except IOError:
                # No joystick found, wait for a bit before trying again
                print('Unable to find any joysticks')
                sleep(1.0)

print("Creating PS4 Joypad service")
service = PS4ControllerService(RobotSettings())
print("Connecting")
client = service_base.connect(service)
print("Connected. Starting loop")
client.loop_start()
service.run()
