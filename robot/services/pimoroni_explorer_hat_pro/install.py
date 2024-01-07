from pyinfra.operations import pip, systemd, files
from robot.common.settings import RobotSettings
settings = RobotSettings()

results = [
    pip.packages(name="install packages", packages=["smbus2", "explorerhat"], present=True, _sudo=True),
    files.put(
        name="Copy the service source code",
        src="robot/services/pimoroni_explorer_hat_pro/service.py",
        dest="robot/services/pimoroni_explorer_hat_pro/service.py",
    ),
    # Create the service unit file
    files.template(
        name="Create explorerhat service",
        src="robot/services/pimoroni_explorer_hat_pro/service.j2",
        dest="/etc/systemd/system/explorerhat.service",
        mode="644",
        user="root",
        group="root",
        pi_username=settings.pi_username,
        _sudo=True
    )
]


# Enable the service
if any(result.changed for result in results):
    systemd.service(
        name="Enable explorerhat service",
        service="explorerhat.service",
        enabled=True,
        restarted=True,
        _sudo=True
    )
