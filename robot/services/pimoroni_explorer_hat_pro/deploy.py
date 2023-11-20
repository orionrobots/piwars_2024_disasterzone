from deployment.helpers import system_pip

system_pip(
    name="SMBus and explorer hat", 
    packages=[
        "smbus2",
        "explorerhat",
    ])
