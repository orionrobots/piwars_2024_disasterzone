# Install tasks for fabric
from fabric import task
from invoke import Collection

@task
def setup_pimoroni_explorer_hat_pro(c):
    # maybe need RPI.GPIO
    c.sudo("pip3 install --upgrade smbus2 explorerhat")

@task
def install(c):
    # run the setup task above
    setup_pimoroni_explorer_hat_pro(c)
    c.put("pimoroni_explorer_hat_pro/robot.py", "src/robot.py")

pimoroni_explorer_hat_pro = Collection("pimoroni_explorer_hat_pro")
pimoroni_explorer_hat_pro.add_task(install, "install")