# Install tasks for fabric
from fabric import task
from invoke import Collection
from io import BytesIO

@task
def setup_dfrobot_library(c):
    library_source = "https://github.com/DFRobot/DFRobot_RaspberryPi_Expansion_Board.git"
    ref = "d83c356e6f2b33b4eee4cc1f3a78ee10006abc5f" # master V1.0.0
    c.run(f"git clone {library_source}")
    with c.cd("DFRobot_RaspberryPi_Expansion_Board"):
        c.run(f"git checkout {ref}")
        # no installer for this
    # check if this library is in the PYTHON_PATH
    config_file = BytesIO()
    c.get("~/.bashrc", config_file) 
    if b"DFRobot_RaspberryPi_Expansion_Board" not in config_file.getvalue():
            # if not, add it to the PYTHON_PATH
            config_file.write("export PYTHONPATH=$PYTHONPATH:~/DFRobot_RaspberryPi_Expansion_Board")
            c.put(config_file, "~/.bashrc")

@task
def install(c):
    # run the setup task above
    setup_dfrobot_library(c)
    c.copy("dfrobot_gravity/robot.py", "robot.py")

dfrobot_gravity = Collection("dfrobot_gravity")
dfrobot_gravity.add_task(install, "install")
