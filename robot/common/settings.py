from pydantic import SecretStr
from pydantic_settings import BaseSettings

class RobotSettings(BaseSettings):
    pi_hostname: str
    pi_username: str
    mqtt_username: str
    mqtt_password: SecretStr
    mqtt_port: int = 9001
    board_name: str
    needs_system_pip: bool = True

    class Config:
        env_file = ".env"
