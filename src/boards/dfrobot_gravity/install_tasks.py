# Install tasks for fabric
from fabric import task
from invoke import Collection
import patchwork.files

@task
def setup_dfrobot_library(c):
    if not patchwork.files.exists(c, "DFRobot_RaspberryPi_Expansion_Board"):
        library_source = "https://github.com/DFRobot/DFRobot_RaspberryPi_Expansion_Board.git"
        ref = "d83c356e6f2b33b4eee4cc1f3a78ee10006abc5f" # master V1.0.0
        c.run(f"git clone {library_source}")
        with c.cd("DFRobot_RaspberryPi_Expansion_Board"):
            c.run(f"git checkout {ref}")

@task
def install(c):
    # run the setup task above
    setup_dfrobot_library(c)
    print("Updating code on robot")
    c.put("dfrobot_gravity/robot.py", "src/robot.py")

dfrobot_gravity = Collection("dfrobot_gravity")
dfrobot_gravity.add_task(install, "install")
