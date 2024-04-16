# Launcher service

An MQTT service to launch/stop other services.
Can also power down the Raspberry Pi.

## Messages and topics

- launcher/start 'service_name' : Start the service 'service_name'
- launcher/stop 'service_name' : Stop the service 'service_name'
- launcher/poweroff : Power off the Raspberry Pi
