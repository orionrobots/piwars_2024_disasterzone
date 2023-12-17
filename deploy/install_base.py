from pyinfra.operations import apt, server, files

# install python tools, git, gpiozero, smbus
base_packages = apt.packages(
    name="Install python tools, git, gpiozero, smbus",
    packages=["python3-pip", "python3-smbus", "i2c-tools", "git", "python3-gpiozero"],
    present=True,
    _sudo=True,
)

if base_packages.changed:
    server.reboot(_sudo = True)

server.shell("raspi-config nonint do_i2c 0") # Option 0 - enabled

# Copy the environment file
files.put(
    src=".env",
    dest="/etc/robot.env",
    _sudo=True
)
