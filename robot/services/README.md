# Services

These are robot mqtt services.

Each should have the following:

- notes.md -> Notes on the device/board/algorithm.
- service.py -> Main service code.
- install.py -> PyInfra code to install the service and dependencies.
    - Should include installing a systemd unit file, and restarting if necessary.
- service.j2 -> template for the service systemd file.

## Sending a message to a service

To send a message to a service, publish to the topic:

```bash
source /etc/robot.env 
mosquitto_pub -t "motors/forward" -m '{"speed": 1}' -u $MQTT_USERNAME -P $MQTT_PASSWORD
```

Robot.env is deployed from your .env, and will contain the needed secrets for mqtt access.
