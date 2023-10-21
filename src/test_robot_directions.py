from robot import Robot
import time

robot = Robot()
speed = 0.8

print("left")
robot.left(speed)
time.sleep(0.5)
robot.stop()
time.sleep(0.2)
print("right")
robot.right(speed)
time.sleep(0.5)
robot.stop()
time.sleep(0.2)
print("forward")
robot.forward(speed)
time.sleep(0.5)
robot.stop()
time.sleep(0.2)
print("backward")
robot.backward(speed)
time.sleep(0.5)
print("stop")
robot.stop()
