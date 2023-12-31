from robot.common.settings import RobotSettings

settings = RobotSettings()

robots = [
    (settings.pi_hostname, {
        "ssh_user": settings.pi_username, 
        "board_name": settings.board_name
    })
]
