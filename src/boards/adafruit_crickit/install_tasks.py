# Install tasks for fabric
from fabric import task
from invoke import Collection

@task
def setup_adafruit_crickit(c):
    # maybe need RPI.GPIO
    c.sudo("pip3 install Adafruit-Blinka")
    c.run("pip3 install adafruit-circuitpython-crickit")

@task
def install(c):
    # run the setup task above
    setup_adafruit_crickit(c)
    c.put("adafruit_crickit/robot.py", "src/robot.py")
    c.put("adafruit_crickit/test_crickit_motors.py")

adafruit_crickit = Collection("adafruit_crickit")
adafruit_crickit.add_task(install, "install")
