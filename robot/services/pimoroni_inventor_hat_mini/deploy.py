from deployment.helpers import system_pip

system_pip(
    name="Install Inventor hat mini dependancies",
    packages=[
        "smbus2",
        "inventorhatmini"
    ]
)
