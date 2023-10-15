# Install tasks for fabric
from fabric import task
from invoke import Collection

@task
def setup_adafruit_stepper_motor_hat(c):
    # maybe need RPI.GPIO
    c.sudo("pip3 install Adafruit-Blinka")
    c.sudo("pip3 install adafruit-circuitpython-motorkit")


@task
def install(c):
    # run the setup task above
    setup_adafruit_stepper_motor_hat(c)
    c.put("adafruit_stepper_motor_hat/robot.py", "robot.py")

adafruit_stepper_motor_hat = Collection("adafruit_stepper_motor_hat")
adafruit_stepper_motor_hat.add_task(install, "install")
