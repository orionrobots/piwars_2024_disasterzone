from pyinfra.operations import server, python

result = server.shell("/usr/sbin/i2cdetect -y 1")
def log_output():
    print(result.stdout)
python.call(log_output)
