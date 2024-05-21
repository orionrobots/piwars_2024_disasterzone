from time import sleep
from subprocess import call

from approxeng.input.selectbinder import ControllerResource
from paho.mqtt.client import MQTTMessage, Client

from robot.common import service_base
from robot.common.settings import RobotSettings

ROLLERS_SPEED = 0.7
TRIGGER_FIRING_POSITION = -50
PAN_SCALE = -5
TILT_SCALE = -4
GRABBER_UP_POSITION = 20
GRABBER_DOWN_POSITION = 80
PAN_MAX = 45
TILT_MAX = 45

class PS4ControllerService(service_base.ServiceBase):
    name = "ps4_joypad"
    aim_x = 0
    aim_y = 0
    camera_stream_running = False
    line_following_running = False

    def __init__(self, settings: RobotSettings) -> None:
        self.settings = settings
        super().__init__()

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        print("Subscribing")
        client.subscribe("yukon/button_a")
        client.message_callback_add("yukon/button_a", self.connect_attempt)

    def connect_attempt(self, client: Client, userdata, msg: MQTTMessage):
        call(f"bluetoothctl connect {self.settings.ps4_mac_address}", shell=True)

    def run(self):
        motors_centered = False
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
                        if joystick.rx != 0 or joystick.ry != 0:
                            self.aim_x += joystick.rx * PAN_SCALE
                            self.aim_y += joystick.ry * TILT_SCALE
                            # Keep to limits
                            if self.aim_x > PAN_MAX:
                                self.aim_x = PAN_MAX
                            elif self.aim_x < -PAN_MAX:
                                self.aim_x = -PAN_MAX
                            if self.aim_y > TILT_MAX:
                                self.aim_y = TILT_MAX
                            elif self.aim_y < -TILT_MAX:
                                self.aim_y = -TILT_MAX
                            self.publish_json("servos/set", {"index": 0, "position": self.aim_x})
                            self.publish_json("servos/set", {"index": 1, "position": self.aim_y})
                        joystick.check_presses()
                        if "r1" in joystick.presses:
                            self.publish_json("servos/move", {"index": 3, "position": GRABBER_UP_POSITION})
                        if "l1" in joystick.presses:
                            self.publish_json("servos/move", {"index": 3, "position": GRABBER_DOWN_POSITION})
                        if "r2" in joystick.presses:
                            self.publish_json("servos/set", {"index": 2, "position": TRIGGER_FIRING_POSITION})
                        elif "r2" in joystick.releases:
                            self.publish_json("servos/set", {"index": 2, "position": 0})
                        if "l2" in joystick.presses:
                            self.publish_json("dual_motors/set", {"speed": ROLLERS_SPEED, "index": 0})
                        elif "l2" in joystick.releases:
                            self.publish_json("dual_motors/stop", {"index": 0})
                        if joystick["select"] and joystick["start"] and joystick["triangle"]:
                            self.publish_json("launcher/poweroff", {})
                        elif "triangle" in joystick.presses:
                            self.publish_json("all/stop", {})
                        if "home" in joystick.presses:
                            self.publish_json("launcher/restart", "yukon")
                        if "square" in joystick.presses:
                            if self.camera_stream_running:
                                self.publish_json("launcher/stop", "camera_stream")
                                self.camera_stream_running = False
                            else:
                                self.publish_json("launcher/start", "camera_stream")
                                self.camera_stream_running = True
                        if "circle" in joystick.presses:
                            if self.line_following_running:
                                self.publish_json("launcher/stop", "line_following")
                                self.line_following_running = False
                            else:
                                self.publish_json("launcher/start", "line_following")
                                self.line_following_running = True

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
