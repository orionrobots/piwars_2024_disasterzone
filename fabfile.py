from fabric import task

@task
def deploy_system(c):
    c.sudo("apt-get install -y python3-pip python3-smbus i2c-tools git")
    c.sudo("raspi-config nonint do_i2c 0") # 0 enables interface
    c.sudo("apt-get update")
    c.sudo("apt-get upgrade -y")
    c.sudo("reboot")

@task
def deploy_adafruit_stepper_motor_hat(c):
    # maybe need RPI.GPIO
    c.sudo("pip3 install Adafruit-Blinka")
    c.sudo("pip3 install adafruit-circuitpython-motorkit")

@task
def show_i2c_devices(c):
    c.run("/usr/sbin/i2cdetect -y 1")
    c.run("/usr/sbin/i2cdetect -y 0")

@task
def power_off(c):
    c.sudo("poweroff")
