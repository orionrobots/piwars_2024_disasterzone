from pyinfra import local, host

board = host.data.get("board")
board_path = f"robot/boards/{board}/install_tasks.py"
local.include(board_path)