from robot import Robot
import time

robot = Robot()
speed = 0.8

print("Left motor only")
robot.value = (speed, 0)
time.sleep(0.5)
robot.stop()
time.sleep(0.2)

print("Right motor only")
robot.value = (0, speed)
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
print("Spin left")
robot.left(speed)
time.sleep(0.5)
robot.stop()
time.sleep(0.2)
print("Spin right")
robot.right(speed)
time.sleep(0.5)
robot.stop()
time.sleep(0.2)
print("stop")
robot.stop()
