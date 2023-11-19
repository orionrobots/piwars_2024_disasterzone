from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    pi_hostname: str = "your_robot"
    pi_username: str = "your_username"
    mqtt_host: str = "localhost"
    mqtt_username: str = "your_mqtt"
    mqtt_password: str = "your_mqtt_pass"


# TODO: Add motor controller choice here
