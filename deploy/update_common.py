from pyinfra.operations import files

common_files = files.sync("robot/common", "robot/common")
environment = files.put(
        name="Copy the environment file",
        src=".env",
        dest="/etc/robot.env",
        _sudo=True
    )

common_changed = common_files.changed or environment.changed
