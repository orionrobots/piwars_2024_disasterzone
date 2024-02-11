import functools

from pyinfra.operations import pip

from robot.common.settings import RobotSettings

settings = RobotSettings()

if settings.needs_system_pip:
    pip_extra_install_args="--root-user-action ignore --break-system-packages"
else:
    pip_extra_install_args=""

system_pip = functools.partial(pip.packages, 
                               extra_install_args=pip_extra_install_args)
