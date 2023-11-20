import functools

from pyinfra.operations import \
    apt, pip, files, systemd, server
from pyinfra import host

system_pip = functools.partial(pip.packages, extra_install_args="--root-user-action ignore --break-system-packages")
needs_reboot = False

# install python tools, git, gpiozero, smbus
base_packages = apt.packages(
    name="Install python tools, git, gpiozero, smbus",
    packages=["python3-pip", "python3-smbus", "i2c-tools", "git", "python3-gpiozero"],
    present=True,
    _sudo=True,
)

needs_reboot = needs_reboot or base_packages.changed

# Check which i2c we'll support
if host.data.get("i2c_type") == "real":
    # enable real i2c
    server.shell("raspi-config nonint do_i2c 0") # Option 0 - enabled
else:
    server.shell("raspi-config nonint do_i2c 1") # Option 1 - disabled
    # Let's make clock stretching work
    overlay_line = "dtoverlay=i2c-gpio,bus=1,i2c_gpio_sda=02,i2c_gpio_scl=03"
    updated_overlay = files.line(
        name="Add i2c overlay to /boot/config.txt",
        path="/boot/config.txt",
        line=overlay_line,
        present=True,
        _sudo=True,
    )
    needs_reboot = needs_reboot or updated_overlay.changed
# Reboot if we need before continuing
if needs_reboot:
    server.reboot(
        name="Reboot to apply changes",
        _sudo=True,
    )

# Install pydantic
system_pip(
    name="Install pydantic",
    packages=["pydantic", "pydantic-settings"],
    present=True,
)

# Deploy mqtt
mosquitto_packages = apt.packages(
    name="Install mosquitto", 
    packages=[
        "mosquitto", 
        "mosquitto-clients"],
    present=True, _sudo=True)
mosquitto_files = files.put(
    name="Configure mosquitto",
    src="deployment/robot_mosquitto.conf",
    dest="/etc/mosquitto/conf.d/robot.conf",
    _sudo=True,
)
if mosquitto_packages:
    # set mosquitto password
    server.shell("sudo mosquitto_passwd -b /etc/mosquitto/passwd robot robot", _sudo=True)
if mosquitto_packages or mosquitto_files:
    # restart mosquitto
    systemd.service(
        name="Restart mosquitto",
        service="mosquitto",
        running=True,
        restarted=True,
        daemon_reload=True,
        _sudo=True,
    )

system_pip(name="Install paho-mqtt", packages=["paho-mqtt"], present=True)

## Web control
system_pip(name="Install web-control dependancies", packages=["fastapi", "uvicorn"], present=True)
