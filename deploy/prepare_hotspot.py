from pyinfra.operations import files
from robot.common.settings import RobotSettings

# Load settings from .env file
settings = RobotSettings()

# Ensure wpa supplicant has a network block for the hotspot
# files.block(
#     name="Ensure network block for hotspot",
#     path="/etc/wpa_supplicant/wpa_supplicant.conf",
#     after=True,
#     line="update_config=1",
#     content=f'network={{\n    ssid=\\"{settings.hotspot_ssid}\\"\n    psk=\\"{settings.hotspot_password.get_secret_value()}\\"\n}}',
#     try_prevent_shell_expansion=True,
#     present=True,
#     _sudo=True,
# )
# This does not yet work.
"""
{
    ssid="{settings.hotspot_ssid}"
    psk="{settings.hotspot_password.get_secret_value()}"
}
"""
