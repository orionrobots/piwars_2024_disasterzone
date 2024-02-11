from robot import Robot
import time

robot = Robot()

for n in range(1, 10):
    robot.forward(n / 10)
    time.sleep(0.5)
robot.stop()
