# Install tasks for fabric
from fabric import task, Connection
from invoke import Collection

host: Connection = None

@task
def install(c):
    # run the setup task above
    host.sudo("pip3 install Adafruit-Blinka")
    host.run("pip3 install adafruit-circuitpython-crickit")
    host.put("adafruit_crickit/robot.py", "src/robot.py")
    host.put("adafruit_crickit/test_crickit_motors.py")

adafruit_crickit = Collection("adafruit_crickit")
adafruit_crickit.add_task(install, "install")
