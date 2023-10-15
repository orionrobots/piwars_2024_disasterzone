# Install tasks for fabric
from fabric import task
from invoke import Collection

@task
def setup_dfrobot_library(c):
    if not c.run("ls DFRobot_RaspberryPi_Expansion_Board"):
        library_source = "https://github.com/DFRobot/DFRobot_RaspberryPi_Expansion_Board.git"
        ref = "d83c356e6f2b33b4eee4cc1f3a78ee10006abc5f" # master V1.0.0
        c.run(f"git clone {library_source}")
        with c.cd("DFRobot_RaspberryPi_Expansion_Board"):
            c.run(f"git checkout {ref}")
    # no installer for this
    # check if this library is in the PYTHON_PATH
    env_line = "export PYTHONPATH=$PYTHONPATH:~/DFRobot_RaspberryPi_Expansion_Board"
    c.run(f"grep -qF 'DFRobot_RaspberryPi_Expansion_Board' ~/.bashrc || echo '{env_line}' >> ~/.bashrc")

@task
def install(c):
    # run the setup task above
    setup_dfrobot_library(c)
    c.put("dfrobot_gravity/robot.py", "robot.py")

dfrobot_gravity = Collection("dfrobot_gravity")
dfrobot_gravity.add_task(install, "install")
