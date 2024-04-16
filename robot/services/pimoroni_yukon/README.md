# Pimoroni Yukon robot service

Slot usage plans:
- Slots 2 and 4 are motors + encoders
- 4 is an LED Strip
- 5 Servo motors


| Other services | --> | MQTT Broker (Mosquitto) | --> | Yukon Service (Runing on the Pi) | --> Serial port ==> | Yukon |

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

## Mounting and reflashing the firmware on the RP2040 on Yukon

From time to time, a micropython firmware update may be needed. This is how you do it:

- Download the latest firmware for Yukon.
- Stop the yukon service with: `sudo systemctl stop yukon`
- Power off the yukon.
- Hold the boot/user button and power it on.
- `sudo mkdir -p /mnt/pico`
- `sudo mount  sudo mount /dev/sda1 /mnt/pico`
- `sudo cp <firmware> /mnt/pico`
- `sudo sync`
- `sudo umount /mnt/pico`
- You should probably run the installer here again.

Refer to section 3.2.1 in https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf.

## Updating the Pimoroni yukon libraries

- Stop the yukon service with: `sudo systemctl stop yukon`
- Download the libaries, unzip them.
- cd into the directory.
- mpremote cp lib :
- You probably want to run the install/restart the service now

## Sunfounder Line Follower Module

- https://github.com/sunfounder/SunFounder_Line_Follower
```python
>>> from machine import Pin, I2C
>>> i2c = I2C(0)
>>> i2c.scan()
[17, 32, 38]
>>> [int (n) for n in i2c.readfrom(0x11, 10)]
[0, 12, 0, 33, 0, 17, 0, 16, 0, 9]
>>> [int (n) for n in i2c.readfrom(0x11, 10)]
[0, 182, 0, 169, 0, 162, 0, 219, 0, 175]
>>> i2c.readfrom(0x11, 10)
b'\x00\x0e\x00!\x00\x11\x00\x12\x00\t'
>>> struct.unpack(">HHHHH",  i2c.readfrom(0x11, 10))
(13, 13, 15, 16, 7)
>>> struct.unpack(">HHHHH",  i2c.readfrom(0x11, 10))
(11, 123, 389, 406, 327)
```
Device address is 0x11. 0x32 and 0x38 are IO extenders on the Yukon.

## Line Following Module MQTT Protocol
- Control messages topics are 'line_follower/control {"enabled": true}' and 'line_follower/control {"enabled": false}'.
- The line sensor readings are published to 'line_follower/differences' as a JSON object: [0, 0, 0, 0]
