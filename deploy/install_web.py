from pyinfra.operations import pip, files, systemd
import os

# Setup the python components
pip.packages(name="install packages", packages=["fastapi"], present=True)
files.sync("web/service.py", "service.py")

pi_username = os.getenv("PI_USERNAME", "pi")

# Setup the systemd service using systemd
systemd.service(
    name="web",
    present=True,
    enabled=True,
    restarted=True,
    user=pi_username,
    command="python3 service.py",
)

