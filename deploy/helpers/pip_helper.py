import functools

from pyinfra.operations import pip
from pyinfra.facts import server
from pyinfra import host

print(host.get_fact(server.LsbRelease))

system_pip = functools.partial(pip.packages, 
                               extra_install_args="--root-user-action ignore --break-system-packages")
