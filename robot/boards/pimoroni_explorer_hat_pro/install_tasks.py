from pyinfra.operations import pip, files

pip.packages(name="install packages", packages=["smbus2", "explorerhat"], present=True, _sudo=True)

files.put(src="robot/boards/pimoroni_explorer_hat_pro/robot.py", dest="robot/robot.py")
