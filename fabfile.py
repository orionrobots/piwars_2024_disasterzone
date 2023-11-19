import functools

from fabric import task, Connection
from invoke import Collection
import patchwork.transfers
import patchwork.files

from dfrobot_gravity.install_tasks import dfrobot_gravity
from adafruit_crickit.install_tasks import adafruit_crickit
from adafruit_stepper_motor_hat.install_tasks import adafruit_stepper_motor_hat
from redrobotics_redboard.install_tasks import redrobotics_redboard
from pimoroni_inventor_hat_mini.install_tasks import pimoroni_inventor_hat_mini
from pimoroni_explorer_hat_pro.install_tasks import pimoroni_explorer_hat_pro

from robot.robot_settings import Settings
settings = Settings()
host = Connection(settings.pi_hostname, user=settings.pi_username)
host.sudo = functools.partial(host.sudo, echo=True)

def sudo_pip_install(command):
    host.sudo(f"pip3 install --root-user-action ignore --break-system-packages {command}")

@task
def real_i2c(c):
    host.sudo("raspi-config nonint do_i2c 0") # 0 enabled interface

@task
def software_i2c(c):
    """This is needed for clock stretching, eg the bno055"""
    # See - https://gps-pie.com/pi_i2c_config.htm
    # Let's make clock stretching work
    host.sudo("raspi-config nonint do_i2c 1") # 1 disables interface
    overlay_line = "dtoverlay=i2c-gpio,bus=1,i2c_gpio_sda=02,i2c_gpio_scl=03"
    if not patchwork.files.contains(c,"/boot/config.txt", overlay_line):
        host.sudo(f"echo {overlay_line} | sudo tee -a /boot/config.txt > /dev/null")

@task
def deploy_system(c):
    host.sudo("apt-get update")
    host.sudo("apt-get upgrade -y")
    host.sudo("apt-get install -y python3-pip python3-smbus i2c-tools git python3-gpiozero")
    host.sudo("reboot")

@task
def show_i2c_devices(c):
    host.run("/usr/sbin/i2cdetect -y 1")

@task
def power_off(c):
    host.sudo("poweroff")

@task
def put_code(c):
    patchwork.transfers.rsync(host, "robot/", "robot")
    host.put("drive_motors_service/motors_service.py", "robot/motors_service.py")

@task
def put_env_config(c):
    host.put(".env", ".env")

@task
def deploy_pydantic(c):
    sudo_pip_install("--upgrade pydantic pydantic-settings")

@task(pre=[deploy_pydantic, put_env_config])
def deploy_mqtt(c):
    """MQTT can be used to create a service bus"""
    host.sudo("apt-get install -y mosquitto mosquitto-clients")
    print("Setting password. No echo")
    file_lines = [
        "listener 1883",
        "protocol mqtt",
        "# Websockets",
        "listener 9001",
        "protocol websockets",
    ]
    host.sudo("rm /etc/mosquitto/conf.d/websockets.conf")
    for line in file_lines:
        host.sudo(f"echo {line} | sudo tee -a /etc/mosquitto/conf.d/websockets.conf > /dev/null")

    host.sudo(f"mosquitto_passwd -c -b /etc/mosquitto/passwd {settings.mqtt_username} {settings.mqtt_password}", echo=False)
    sudo_pip_install("paho-mqtt")
    host.sudo("systemctl restart mosquitto")

@task
def deploy_web_control(c):
    sudo_pip_install("--upgrade fastapi uvicorn")

# Add the gravity installer to the root collection
ns = Collection()
def add_module(module):
    module.host = host
    ns.add_collection(module)

add_module(dfrobot_gravity)
add_module(adafruit_crickit)
add_module(adafruit_stepper_motor_hat)
add_module(redrobotics_redboard)
add_module(pimoroni_inventor_hat_mini)
add_module(pimoroni_explorer_hat_pro)

# Add all the tasks above to the root collection
ns.add_task(real_i2c, "real_i2c")
ns.add_task(software_i2c, "software_i2c")
ns.add_task(deploy_system, "deploy_system")
ns.add_task(show_i2c_devices, "show_i2c_devices")
ns.add_task(power_off, "power_off")
ns.add_task(put_code, "put_code")
ns.add_task(deploy_web_control, "deploy_web_control")
ns.add_task(deploy_mqtt, "deploy_mqtt")
ns.add_task(put_env_config, "put_env_config")
