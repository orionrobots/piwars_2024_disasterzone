from pyinfra.operations import pip, files

from deploy.helpers.python_service import deploy_python_service

pip.packages(name="Install packages", packages=['approxeng.input'], _sudo=True)

files.put("robot/services/ps4_joypad/tests/test_joystick_connected.py", "test_joystick_connected.py")


deploy_python_service(
    service_source_file="robot/services/ps4_joypad/service.py",
    service_module="robot.services.ps4_joypad.service",
    service_name="ps4_joypad",
    service_description="PS4 Joypad service",
    _sudo=True
)
