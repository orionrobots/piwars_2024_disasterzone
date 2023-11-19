# Install tasks for fabric
from fabric import task, Connection
from invoke import Collection

host: Connection = None

@task
def install(c):
    print("Updating code on robot")
    host.put("redrobotics_redboard/robot.py", "src/robot.py")

redrobotics_redboard = Collection("redrobotics_redboard")
redrobotics_redboard.add_task(install, "install")
