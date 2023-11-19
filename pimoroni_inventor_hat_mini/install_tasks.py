# Install tasks for fabric
from fabric import task, Connection
from invoke import Collection

host: Connection = None

@task
def install(c):
    # run the setup task above
    host.sudo("pip3 install smbus2 inventorhatmini")
    host.put("pimoroni_inventor_hat_mini/robot.py", "src/robot.py")

pimoroni_inventor_hat_mini = Collection("pimoroni_inventor_hat_mini")
pimoroni_inventor_hat_mini.add_task(install, "install")
