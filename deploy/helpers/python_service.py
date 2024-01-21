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
        src=service_source_file,
        dest=service_source_file,
    )
    made_changes = False
    for command in source_file_update:
        made_changes = command
        yield command
    # Create the service unit file
    service_file_update = files.template(
        src="deploy/helpers/python_service.j2",
        dest=f"/etc/systemd/system/{service_name}.service",
        mode="644",
        user="root",
        group="root",
        pi_username=settings.pi_username,
        service_module=service_module,
        service_name=service_name,
        service_description=service_description,
    )
    service_changed = False
    for command in service_file_update:
        service_changed = command
        yield command
    # Enable and restart the service
    yield from systemd.service(
        service=f"{service_name}.service",
        enabled=True,
        restarted=made_changes or service_changed or update_common.common_changed,
        daemon_reload=service_changed,
    )
