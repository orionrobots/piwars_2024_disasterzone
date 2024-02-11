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

files.link(
    name="Link the environment file",
    target="/etc/robot.env",
    path="~/.env",
)

common_changed = common_files.changed or environment.changed or any(package.changed for package in common_pip_packages)
