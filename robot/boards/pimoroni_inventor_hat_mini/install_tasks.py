# Install tasks for fabric
from fabric import task
from invoke import Collection

@task
def setup_pimoroni_inventor_hat_mini(c):
    # maybe need RPI.GPIO
    c.sudo("pip3 install smbus2 inventorhatmini")

@task
def install(c):
    # run the setup task above
    setup_pimoroni_inventor_hat_mini(c)
    c.put("pimoroni_inventor_hat_mini/robot.py", "robot/robot.py")

pimoroni_inventor_hat_mini = Collection("pimoroni_inventor_hat_mini")
pimoroni_inventor_hat_mini.add_task(install, "install")
