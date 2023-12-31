from pyinfra import local
from robot.common.settings import Settings

settings = Settings()

board_path = f"robot/services/{settings.board_name}/install.py"
local.include(board_path)
