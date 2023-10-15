from robot import Robot
import time

robot = Robot()

robot.forwards()
time.sleep(3)
robot.backwards()
time.sleep(3)
robot.right()
time.sleep(3)
robot.left()
time.sleep(3)
robot.stop()
