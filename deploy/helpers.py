import functools

from pyinfra.operations import pip

system_pip = functools.partial(pip.packages, extra_install_args="--root-user-action ignore --break-system-packages")
