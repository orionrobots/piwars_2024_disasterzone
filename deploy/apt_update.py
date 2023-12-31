from pyinfra.operations import \
    apt
# update
apt.update(
    name="Update apt cache",
    _sudo=True,
)
upgrade = apt.upgrade(
    name="Upgrade all packages",
    _sudo=True,
)