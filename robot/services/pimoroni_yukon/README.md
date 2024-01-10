# Pimoroni Yukon robot service

Slot usage plans:
- Slots 2 and 4 are motors + encoders
- 4 is an LED Strip
- 5 Servo motors

## Links and docs

- https://github.com/pimoroni/yukon/blob/main/docs/reference.md#pimoroni_yukon-reference
- https://pythonhosted.org/pyserial/examples.html#tcp-ip-serial-bridge
- https://forum.micropython.org/viewtopic.php?t=11336
- https://shop.pimoroni.com/products/yukon?variant=41185258111059
- https://shop.pimoroni.com/products/big-motor-encoder-module-for-yukon?variant=41186939437139
- https://pypi.org/project/mpremote/

## Communication

Currently, the firmware on the Yukon is Micropython based. Over USB that only offers a single REPL/Serial.
We will do the follwoing:
- Use MPRemote to start/stop/deploy code.
- When it is running, use the repl to send commands to this part of the robot.

The communication protocol can be nice and simple. Since we are working with MQTT, we can translate to serial:
- The service subscribes to topics.
- Any topic it's subscribed to is passed on to the robot - topic/name:payload 
- An end of payload is denoted by what? Its a line for now. topic/name:payload\n.
- Any serial responses are published to the topic: topic/name:payload

The commands for the motor will be the same as other motor services here.
