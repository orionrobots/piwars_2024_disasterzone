from pyinfra.operations import systemd, files
from deploy.helpers import system_pip
from robot.common.settings import RobotSettings
from deploy import deploy_common_environment
settings = RobotSettings()

results = [
    deploy_common_environment.common_packages,
    deploy_common_environment.environment_file,
    deploy_common_environment.common_folder,
    system_pip(name="install packages", packages=["smbus2", "inventorhatmini"], present=True, _sudo=True),
    
    # Update the service source code
    files.put(
        name="Copy the service source code",
        src="robot/services/pimoroni_inventor_hat_mini/service.py",
        dest="robot/services/pimoroni_inventor_hat_mini/service.py",
    ),
    # Create the service unit file
    files.template(
        name="Create inventorhatmini service",
        src="deploy/service_template.j2",
        dest="/etc/systemd/system/inventorhatmini.service",
        mode="644",
        user="root",
        group="root",
        pi_username=settings.pi_username,
        restart="always",
        service_module="robot.services.pimoroni_inventor_hat_mini.service",
        service_description="Inventor Hat Mini service",
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
