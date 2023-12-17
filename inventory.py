from robot.common.settings import RobotSettings

settings = RobotSettings()

robots = [
    (settings.pi_hostname, {
        "ssh_user": settings.pi_username, 
        "board_name": settings.board_name,
        "mqtt_username": settings.mqtt_username,
        "mqtt_password": settings.mqtt_password.get_secret_value()
    })
]

print(robots)
