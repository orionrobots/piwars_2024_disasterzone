from robot.services.common.base_service import BaseService

service = BaseService("demo")
service.run()
service.client.loop_forever()
# could be loop(1) with some work
