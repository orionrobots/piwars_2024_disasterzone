from robot import Robot
import time

robot = Robot()

robot.forward()
time.sleep(0.5)
robot.backwards()
time.sleep(0.5)
robot.right()
time.sleep(0.5)
robot.left()
time.sleep(0.5)
robot.stop()
