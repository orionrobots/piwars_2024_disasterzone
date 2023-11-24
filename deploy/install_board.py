from pyinfra import local
from robot.robot_settings import Settings

settings = Settings()

board_path = f"robot/services/{settings.board_name}/deploy.py"
local.include(board_path)
