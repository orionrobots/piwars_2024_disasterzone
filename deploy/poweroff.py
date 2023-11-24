from pyinfra.operations import server

server.shell("poweroff", _sudo=True)
