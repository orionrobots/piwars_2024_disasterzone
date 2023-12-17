from pyinfra.operations import pip, systemd

pip.packages(name="install packages", packages=["smbus2", "explorerhat"], present=True, _sudo=True)

systemd.service(
    name="ExplorerHat",
    present=True,
    enabled=True,
    restarted=True,
    command="python3 ")
