from deploy.helpers.python_service import deploy_python_service

deploy_python_service(
    service_source_file="robot/services/line_following/service.py",
    service_module="robot.services.line_following.service",
    service_name="line_following",
    service_description="Line following service",
    must_restart=False,
    _sudo=True
)
