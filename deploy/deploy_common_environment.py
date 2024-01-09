from robot.common.settings import RobotSettings
settings = RobotSettings()

from pyinfra.operations import pip, files
from deploy.helpers import system_pip

common_packages = system_pip(name="install packages", packages=["pydantic-settings"], present=True, _sudo=True)

# Update the environment
environment_file = files.put(
    name="Copy the environment file",
    src=".env",
    dest="/etc/robot.env",
    _sudo=True
)

# Update the common folder
common_folder = files.sync(
    name="Copy the common folder",
    src="robot/common",
    dest="robot/common"
)
