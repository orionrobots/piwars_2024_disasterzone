from pyinfra.operations import pip, systemd, files
import os

pip.packages(name="install packages", packages=["smbus2", "explorerhat"], present=True, _sudo=True)

username = os.environ["PI_USERNAME"]

# Create the service unit file
files.template(
    name="Create explorerhat service",
    src="robot/services/pimoroni_explorer_hat/service.j2",
    dest="/etc/systemd/system/explorerhat.service",
    mode="644",
    user="root",
    group="root",
    pi_username=username,
    _sudo=True
)

# Enable the service
systemd.service(
    name="Enable explorerhat service",
    service="explorerhat.service",
    present=True,
    enabled=True,
    restarted=True,
    _sudo=True
)
