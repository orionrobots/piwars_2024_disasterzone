from robot.robot_settings import Settings

settings = Settings()
robot = [
    (settings.pi_hostname, {"ssh_user": settings.pi_username, "i2c_type": "software"})
]
