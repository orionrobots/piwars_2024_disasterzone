from pyinfra.api import operation, StringCommand
from pyinfra.operations import apt, files, systemd
from pyinfra.local import include
from robot.common.settings import RobotSettings
from deploy import deploy_common_environment
settings = RobotSettings()

@operation
def mpremote_sync(name, src, dest):
    """Sync source files to a micropython device
    with mpremote.
    src=local folder
    dest=folder on micropython device attached to the remote robot
    """
    pi_dest = f"mpremote/{dest}"
    # update the robot copy
    files.sync(
        name="Copy the mpremote folder",
        src=src,
        dest=pi_dest
    )
    yield StringCommand(f"mpremote --sync {pi_dest} {dest}")

# For now assume the Yukon has Pimoroni Firmware installed.

results = [
    deploy_common_environment.common_packages,
    deploy_common_environment.environment_file,
    deploy_common_environment.common_folder,
    apt.packages(name="Install packages", packages=['mpremote', 'python3-pyserial'], present=True, _sudo=True),
    mpremote_sync(name="Sync mpremote", src="robot/services/pimoroni_yukon/yukon", dest="/"),
        # Update the service source code
    files.put(
        name="Copy the service source code",
        src="robot/services/pimoroni_yukon/service.py",
        dest="robot/services/pimoroni_yukon/service.py",
    ),
    # Create the service unit file
    files.template(
        name="Create Yukon service",
        src="deploy/service_template.j2",
        dest="/etc/systemd/system/pimoroniyukon.service",
        mode="644",
        user="root",
        group="root",
        pi_username=settings.pi_username,
        restart="always",
        service_module="robot.services.pimoroni_yukon.service",
        service_description="Pimoroni Yukon",
        _sudo=True
    ),
]

# Enable and restart the service
if any(result.changed for result in results):
    systemd.service(
        name="Enable Yukon service",
        service="pimoroniyukon.service",
        enabled=True,
        restarted=True,
        _sudo=True
    )
