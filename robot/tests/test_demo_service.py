"""python -mrobot.tests.test_demo_service"""
from robot.services.common.base_service import BaseService

service = BaseService("test_demo")
service.run()

print("Publishing message")
result = service.client.publish("demo", "hello world")
result.wait_for_publish()
print("Result:", result)
