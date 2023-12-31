from pydantic import SecretStr
from pydantic_settings import BaseSettings

class RobotSettings(BaseSettings):
    pi_hostname: str
    pi_username: str
    mqtt_username: str
    mqtt_password: SecretStr
    board_name: str

    class Config:
        env_file = ".env"
