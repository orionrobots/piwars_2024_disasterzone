from fabric import task

@task
def deploy_system(c):
    c.run("sudo apt-get install -y python3-pip python3-smbus i2c-tools git")
    c.run("sudo raspi-config nonint do_i2c 0")
    c.run("sudo raspi-config nonint do_i2c 1")

@task
def deploy_adafruit_stepper_motor_hat(c):
    c.run("sudo pip3 install Adafruit-Blinka")
    c.run("sudo pip3 install adafruit-circuitpython-motorkit")
