from pyinfra.operations import files

files.sync("robot", "robot", exclude=[".git", ".DS_Store", "__pycache__"])
