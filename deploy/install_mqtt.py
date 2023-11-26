from pyinfra.operations import apt, files, systemd, pip, server

mosquitto_packages = apt.packages(
    name="Install mosquitto", 
    packages=[
        "mosquitto", 
        "mosquitto-clients"],
    present=True, _sudo=True)

mosquitto_files = files.put(
    name="Configure mosquitto",
    src="deploy/robot_mosquitto.conf",
    dest="/etc/mosquitto/conf.d/robot.conf",
    _sudo=True
)

if mosquitto_packages.changed:
    # set mosquitto password
    server.shell("mosquitto_passwd -c -b /etc/mosquitto/passwd robot robot", _sudo=True)

if mosquitto_packages.changed or mosquitto_files.changed:
    # restart mosquitto
    systemd.service(
        name="Restart mosquitto",
        service="mosquitto",
        running=True,
        restarted=True,
        daemon_reload=True,
        _sudo=True,
    )

pip.packages(name="Install paho-mqtt", packages=["paho-mqtt"], present=True, _sudo=True)
