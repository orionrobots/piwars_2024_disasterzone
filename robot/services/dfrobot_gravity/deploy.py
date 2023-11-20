from pyinfra.operations import git

git.repo(
    name="Clone DF Robot RaspberryPi Extension Board repo",
    src="https://github.com/DFRobot/DFRobot_RaspberryPi_Expansion_Board.git",
    dest="DFRobot_RaspberryPi_Expansion_Board",
    branch="d83c356e6f2b33b4eee4cc1f3a78ee10006abc5f" # master V1.0.0
)
