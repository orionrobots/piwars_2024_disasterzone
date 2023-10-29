from fabric import task

def install_bno055(c):
    c.sudo("pip3 install adafruit-circuitpython-bno055")
