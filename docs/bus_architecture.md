# Bus archtiecture

This project will be based on some connected MQTT components, using a mosquitto instance as the the broker.

## Installing

`fab setup_mqtt` -> Will become part of main setup when established

## Libraries

We want this to be asynchronous capable. We will use the asyncio-mqtt library <https://pypi.org/project/asyncio-mqtt/> along with [paho](https://github.com/eclipse/paho.mqtt.python).


## Messages and message types

### Motors

- Topic: `motors/left` and `motors/right`
  payloads: -1.0 to 1.0

- Topic: `motors/values`
  payload: left (-1 to 1.0), right (-1 to 1.0)

- Topic: `motors/forward`
  payload (optional): speed (0 to 1.0)- defaults to 1.0, optional curve (-1 to 1.0) - defaults to 0.0
- Topic: `motors/backward`
  payload (optional): speed (0 to 1.0)- defaults to 1.0, optional curve (-1 to 1.0) - defaults to 0.0
- Topic: `motors/stop`
- Maybe topic `motors/reverse`. Not 100% sure.

Assume 1 second duration, or until next command.


Links:
- https://www.google.com/search?q=mqtt+mosquito+broker+tutorial&oq=mqtt+mosquito+broker+tutorial&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yCAgCEAAYFhgeMggIAxAAGBYYHjIKCAQQABiGAxiKBTIKCAUQABiGAxiKBTIKCAYQABiGAxiKBTIKCAcQABiGAxiKBTIKCAgQABiGAxiKBdIBCDY1NjlqMGo0qAIAsAIA&sourceid=chrome&ie=UTF-8
- https://mosquitto.org/
- https://cedalo.com/blog/configuring-paho-mqtt-python-client-with-examples/
