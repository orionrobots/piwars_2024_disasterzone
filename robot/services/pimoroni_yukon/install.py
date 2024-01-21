


from pyinfra.operations import pip, apt

from deploy.helpers.mpremote_tools import mpremote_sync_file, mpremote_reset
from deploy.helpers.python_service import deploy_python_service

pip.packages(name="Install mpremote", packages=["mpremote"])
# file_sync = mpremote_sync_file(name="Copy test file", src="robot/services/pimoroni_yukon/rp2040/test_flash_leds.py", dest="main.py")
# if file_sync.changed:
#     mpremote_reset(name="Reset the Yukon")

apt.packages(name="Install packages", packages=['python3-serial'], present=True, _sudo=True)

file_sync = mpremote_sync_file(name="Copy main", src="robot/services/pimoroni_yukon/rp2040/main.py", dest="main.py")
if file_sync.changed:
    mpremote_reset(name="Reset the Yukon")

deploy_python_service(
    service_source_file="robot/services/pimoroni_yukon/service.py",
    service_module="robot.services.pimoroni_yukon.service",
    service_name="yukon",
    service_description="Yukon board service",
    _sudo=True
)
