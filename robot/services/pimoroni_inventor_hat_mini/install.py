from pyinfra.operations import pip, systemd, systemd, files
import os

pip.packages(name="install packages", packages=["smbus2", "inventorhatmini"], present=True, _sudo=True)

# Create the service unit file
files.template(
    name="Create inventorhatmini service",
    src="robot/services/pimoroni_inventor_hat_mini/service.j2",
    dest="/etc/systemd/system/inventorhatmini.service",
    mode="644",
    user="root",
    group="root",
    pi_username=os.environ["PI_USERNAME"],
    _sudo=True
)

# Enable the service
systemd.service(
    name="Enable inventorhatmini service",
    service="inventorhatmini.service",
    enabled=True,
    restarted=True,
    _sudo=True
)
