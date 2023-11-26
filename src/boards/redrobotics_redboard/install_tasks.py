# Install tasks for fabric
from fabric import task
from invoke import Collection

@task
def install(c):
    print("Updating code on robot")
    c.put("redrobotics_redboard/robot.py", "src/robot.py")

redrobotics_redboard = Collection("redrobotics_redboard")
redrobotics_redboard.add_task(install, "install")
