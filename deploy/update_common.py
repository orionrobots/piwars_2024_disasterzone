from pyinfra.operations import files
from deploy.helpers.pip_helper import system_pip

common_pip_packages = system_pip(
    name="install common packages", packages=["pydantic-settings"], present=True, _sudo=True),

common_files = files.sync("robot/common", "robot/common")
environment = files.put(
        name="Copy the environment file",
        src=".env",
        dest="/etc/robot.env",
        _sudo=True
    )

common_changed = common_files.changed or environment.changed or common_pip_packages.changed
