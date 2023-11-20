from deployment.helpers import system_pip
from pyinfra.operations import pip

system_pip(name="System blinka and motorkit", 
           packages=["Adafruit-Blinka", "adafruit-circuitpython-motorkit"])
