


from pyinfra.operations import pip, apt, systemd

from deploy.helpers.mpremote_tools import mpremote_sync_file, mpremote_reset
from deploy.helpers.python_service import deploy_python_service

pip.packages(name="Install mpremote", packages=["mpremote"])
apt.packages(name="Install packages", packages=['python3-serial'], present=True, _sudo=True)

# Stop the service to release the serial port
systemd.service(service="yukon", running=False)

file_sync = mpremote_sync_file(name="Copy main", src="robot/services/pimoroni_yukon/rp2040/main.py", dest="main.py")
if file_sync.changed:
    mpremote_reset(name="Reset the Yukon")

deploy_python_service(
    service_source_file="robot/services/pimoroni_yukon/service.py",
    service_module="robot.services.pimoroni_yukon.service",
    service_name="yukon",
    service_description="Yukon board service",
    must_restart=True, # restart, as we stop the service to release the serial port
    _sudo=True
)
