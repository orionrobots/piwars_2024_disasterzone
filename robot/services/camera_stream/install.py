from pyinfra.operations import pip, apt

from deploy.helpers.python_service import deploy_python_service

apt.packages(name="Install apt packages", packages=["python3-picamera2", "python3-numpy", "libopenblas0", "python3-pil" ], _sudo=True)
pip.packages(name="Install pip packages", packages=['bokeh'], _sudo=True)

# puts files in /usr/nclude/opencv4 (not that we need that)

# enable camera with raspi=config

deploy_python_service(
    service_source_file="robot/services/camera_stream/service.py",
    service_module="robot.services.camera_stream.service",
    service_name="camera_stream",
    service_description="Camera stream service",
    auto_start=False,
    _sudo=True
)
