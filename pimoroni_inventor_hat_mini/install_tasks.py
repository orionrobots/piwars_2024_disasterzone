# Install tasks for fabric
from fabric import task, Connection
from invoke import Collection

host: Connection = None

@task
def setup_pimoroni_inventor_hat_mini(c):
    # maybe need RPI.GPIO
    c.sudo("pip3 install smbus2 inventorhatmini")

@task
def install(c):
    # run the setup task above
    setup_pimoroni_inventor_hat_mini(host)
    host.put("pimoroni_inventor_hat_mini/robot.py", "src/robot.py")

pimoroni_inventor_hat_mini = Collection("pimoroni_inventor_hat_mini")
pimoroni_inventor_hat_mini.add_task(install, "install")
