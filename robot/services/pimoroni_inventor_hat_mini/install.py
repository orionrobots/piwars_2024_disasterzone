from pyinfra.operations import pip, systemd, files
from deploy.helpers import system_pip
from robot.common.settings import RobotSettings
settings = RobotSettings()

results = [
    system_pip(name="install packages", packages=["smbus2", "inventorhatmini", "pydantic-settings"], present=True, _sudo=True),

    # Update the environment
    files.put(
        name="Copy the environment file",
        src=".env",
        dest="/etc/robot.env",
        _sudo=True
    ),
    # Update the service source code
    files.put(
        name="Copy the service source code",
        src="robot/services/pimoroni_inventor_hat_mini/service.py",
        dest="robot/services/pimoroni_inventor_hat_mini/service.py",
    ),
    # Update the common folder
    files.sync(
        name="Copy the common folder",
        src="robot/common",
        dest="robot/common"
    ),
    # Create the service unit file
    files.template(
        name="Create inventorhatmini service",
        src="robot/services/pimoroni_inventor_hat_mini/service.j2",
        dest="/etc/systemd/system/inventorhatmini.service",
        mode="644",
        user="root",
        group="root",
        pi_username=settings.pi_username,
        _sudo=True
    )
]

# Enable and restart the service
if any(result.changed for result in results):
    systemd.service(
        name="Enable inventorhatmini service",
        service="inventorhatmini.service",
        enabled=True,
        restarted=True,
        _sudo=True
    )
