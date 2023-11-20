from deployment.helpers import system_pip
from pyinfra.operations import pip

system_pip(name="System blinka", packages=["Adafruit-Blinka"])
pip(name="Crickit", packages=["adafruit-circuitpython-crickit"])
