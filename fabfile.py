from fabric import task
from invoke import Collection
import patchwork.transfers

from dfrobot_gravity.install_tasks import dfrobot_gravity
from adafruit_crickit.install_tasks import adafruit_crickit
from adafruit_stepper_motor_hat.install_tasks import adafruit_stepper_motor_hat

@task
def deploy_system(c):
    c.sudo("apt-get update")
    c.sudo("apt-get upgrade -y")
    c.sudo("apt-get install -y python3-pip python3-smbus i2c-tools git python3-gpiozero")
    c.sudo("raspi-config nonint do_i2c 0") # 0 enables interface
    c.sudo("reboot")

@task
def show_i2c_devices(c):
    c.run("/usr/sbin/i2cdetect -y 1")

@task
def power_off(c):
    c.sudo("poweroff")

@task
def put_code(c):
    patchwork.transfers.rsync(c, "src/", "src")

# Add the gravity installer to the root collection
ns = Collection()
ns.add_collection(dfrobot_gravity)
ns.add_collection(adafruit_crickit)
ns.add_collection(adafruit_stepper_motor_hat)
# Add all the tasks above to the root collection
ns.add_task(deploy_system, "deploy_system")
ns.add_task(show_i2c_devices, "show_i2c_devices")
ns.add_task(power_off, "power_off")
ns.add_task(put_code, "put_code")
