from robot.common.service_base import ServiceBase, connect
from robot.common.settings import RobotSettings
import time
import json

settings = RobotSettings()
client = connect(ServiceBase())
client.loop_start()
client.publish ("motors/forward", json.dumps({"speed":0.8}))
time.sleep(2)
client.publish ("motors/forward", json.dumps({"speed":0.8, "curve":0.5}))
time.sleep(1)
