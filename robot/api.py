# to run: uvicorn api:app --reload --host 0.0.0.0

from fastapi import FastAPI
from robot import Robot
import time

app = FastAPI()
robot = Robot()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/left")
def robot_left(speed: float=1):
    robot.left(speed)
    time.sleep(0.3)
    robot.stop()
    return "ok"

@app.get("/right")
def robot_right(speed: float=1):
    robot.right(speed)
    time.sleep(0.3)
    robot.stop()
    return "ok"

@app.get("/forward")
def robot_forward(speed: float=1):
    robot.forward(speed)
    time.sleep(0.3)
    robot.stop()
    return "ok"

@app.get("/backward")
def robot_backward(speed: float=1):
    robot.backward(speed)
    time.sleep(0.3)
    robot.stop()
    return "ok"
