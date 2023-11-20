from pyinfra.operations import server

server.shell("/usr/sbin/i2cdetect -y 1")
