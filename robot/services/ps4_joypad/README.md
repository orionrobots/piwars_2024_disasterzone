# Playstation 4 JoyPad service

This service allows you to control the robot using a PS4 controller. The intention is to patch the Joystick to emit events to the MQTT bus to control other services.

## Decision

One decision is if the Joypad would emit generic events, like joystick moved, and button press events, or to make it a direct control surface, like the phone app, and emit motors move and similar events directly.

For now, this service will emit direct motor and servo control events.

## Installation

This is a pyinfra based installation. The installation will need the following:

- A PS4 controller.
- You will need to pair and trust this with the Pi. This is a one time operation.
    - Using the command Bluetoothctl from ssh:
```bluetoothctl
discoverable on
pairable on
agent on
default-agent
scan on
```
Wait for the controller to appear, then:
```bluetoothctl
pair <controller mac>
trust <controller mac>
```
- Note the MAC for future use, this will become part of the environment for the Pi.
- The installer will install required packages and the service.

## Service intention

- The service will be started at boot, but will not try to connect the joypad, or issue commands until a Yukon/button a press occurs. At this point, it will do a bluetoothctl connect command, wait a short time, and seek the controller device.
- It will then havea  main loop issuing commands on stick events.

## Mappings

The mappings are as follows:
- Left analog stick: control the wheels/tracks
- Right analog stick: control servo 0,1 - pan and tilt on the nerf turret
- Left trigger held: Arm the rollers. When it's released, the rollers will stop.
- Right trigger: Fire the nerf dart
- Triangle: Stop all motors
