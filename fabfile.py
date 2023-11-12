from fabric import task
from invoke import Collection
import patchwork.transfers
import patchwork.files

from dfrobot_gravity.install_tasks import dfrobot_gravity
from adafruit_crickit.install_tasks import adafruit_crickit
from adafruit_stepper_motor_hat.install_tasks import adafruit_stepper_motor_hat
from redrobotics_redboard.install_tasks import redrobotics_redboard
from pimoroni_inventor_hat_mini.install_tasks import pimoroni_inventor_hat_mini
from pimoroni_explorer_hat_pro.install_tasks import pimoroni_explorer_hat_pro

@task
def real_i2c(c):
    c.sudo("raspi-config nonint do_i2c 0") # 0 enabled interface

@task
def software_i2c(c):
    """This is needed for clock stretching, eg the bno055"""
    # See - https://gps-pie.com/pi_i2c_config.htm
    # Let's make clock stretching work
    c.sudo("raspi-config nonint do_i2c 1") # 1 disables interface
    overlay_line = "dtoverlay=i2c-gpio,bus=1,i2c_gpio_sda=02,i2c_gpio_scl=03"
    if not patchwork.files.contains(c,"/boot/config.txt", overlay_line):
        c.sudo(f"echo {overlay_line} | sudo tee -a /boot/config.txt > /dev/null")

@task
def deploy_system(c):
    c.sudo("apt-get update")
    c.sudo("apt-get upgrade -y")
    c.sudo("apt-get install -y python3-pip python3-smbus i2c-tools git python3-gpiozero")        
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

@task
def deploy_web_control(c):
    c.sudo("pip3 install --upgrade fastapi uvicorn")

# Add the gravity installer to the root collection
ns = Collection()
ns.add_collection(dfrobot_gravity)
ns.add_collection(adafruit_crickit)
ns.add_collection(adafruit_stepper_motor_hat)
ns.add_collection(redrobotics_redboard)
ns.add_collection(pimoroni_inventor_hat_mini)
ns.add_collection(pimoroni_explorer_hat_pro)

# Add all the tasks above to the root collection
ns.add_task(real_i2c, "real_i2c")
ns.add_task(software_i2c, "software_i2c")
ns.add_task(deploy_system, "deploy_system")
ns.add_task(show_i2c_devices, "show_i2c_devices")
ns.add_task(power_off, "power_off")
ns.add_task(put_code, "put_code")
ns.add_task(deploy_web_control, "deploy_web_control")
