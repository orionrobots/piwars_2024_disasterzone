"""Deploy helper for deploying a service.
Works as an opperation. 
Depends on common code, settings.
Install the service if it's missing and enable it.
If they, or the service definition are different, restart the service.
"""
import deploy.update_common as update_common

from pyinfra.api import operation
from pyinfra.operations import files, systemd

from robot.common.settings import RobotSettings
settings = RobotSettings()

@operation
def deploy_python_service(service_source_file, service_module, service_name, service_description):
    """Deploy a python service to the robot."""
    # Update the service source file
    source_file_update = files.put(
        name="Copy the service source code",
        src=service_source_file,
        dest=service_source_file,
    )
    yield from source_file_update
    # Create the service unit file
    service_file_update = files.template(
        name=f"Create {service_name} service",
        src="deploy/helpers/python_service.j2",
        dest=f"/etc/systemd/system/{service_name}.service",
        mode="644",
        user="root",
        group="root",
        pi_username=settings.pi_username,
        service_module=service_module,
        service_name=service_name,
        service_description=service_description,
        _sudo=True
    )
    yield from service_file_update
    # Enable and restart the service
    yield from systemd.service(
        name=f"Enable {service_name} service",
        service=f"{service_name}.service",
        enabled=True,
        restarted=source_file_update.changed or service_file_update.changed or update_common.common_changed,
        _sudo=True
    )
