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
def deploy_python_service(service_source_file, service_module, service_name, service_description, must_restart=False,
                          auto_start=True):
    """Deploy a python service to the robot.
    service_source_file is the source python file for the service
    service_module is the python module for the service - the source file but from the top folder with dots
    service_name is the name of the service for use in systemd
    service_description is the description of the service for use in systemd - human readable
    must_restart is a flag to force a restart of the service, even if nothing has changed
    auto_start is a flag to have this service automatically start. Set to false if expected to be started by the launcher
    """
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
    print("service_changed:", service_changed,
          "made_changes:", made_changes,
          "common_changed:", update_common.common_changed)
    yield from systemd.service(
        service=f"{service_name}.service",
        enabled=auto_start,
        restarted=auto_start and (must_restart or made_changes or service_changed or update_common.common_changed),
        running=auto_start,
        daemon_reload=service_changed,
    )
