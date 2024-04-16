from deploy.helpers.python_service import deploy_python_service


deploy_python_service(
    service_source_file="robot/services/launcher/service.py",
    service_module="robot.services.launcher.service",
    service_name="launcher",
    service_description="Launcher service",
    _sudo=True
)
