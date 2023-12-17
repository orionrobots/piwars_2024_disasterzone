from pyinfra.operations import pip, files

pip.packages(name="install packages", packages=["smbus2", "inventorhatmini"], present=True, _sudo=True)

# Install the service
# Add the service to the systemd services

files.put(src="robot/boards/pimoroni_explorer_hat_pro/robot.py", dest="robot/robot.py")
