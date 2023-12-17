from pyinfra import local, host

board_name = host.data.get("board_name")
board_path = f"robot/boards/{board_name}/install_tasks.py"
local.include(board_path)
