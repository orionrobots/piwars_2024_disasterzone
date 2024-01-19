


from pyinfra.operations import files, pip, apt

from deploy.helpers.mpremote_tools import mpremote_sync_file
from deploy.helpers.mpremote_tools import mpremote_reset

pip.packages(name="Install mpremote", packages=["mpremote"])
file_sync = mpremote_sync_file(name="Copy test file", src="robot/services/pimoroni_yukon/rp2040/test_flash_leds.py", dest="main.py")
if file_sync.changed:
    mpremote_reset(name="Reset the Yukon")

# apt.packages(name="Install packages", packages=['python3-pyserial'], present=True, _sudo=True)

# file_sync = mpremote_sync_file(name="Copy main", src="robot/services/pimoroni_yukon/rp2040/main.py", dest="main.py")
# if file_sync.changed:
#     mpremote_reset(name="Reset the Yukon")

# files.copy(name="Copy service,")