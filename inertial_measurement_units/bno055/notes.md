# BNO055 Inertial measurement Unit

The BNO055 gives absolute orientation. You can use this to get Euler (X, Y, Z) angles. For a rover robot, we are mostly interested in the Yaw.

## Clock Stretching

The BNO055 uses clock stretching. This is not compatible with the Raspberry Pi's Broadcom based harware i2c. However, there's a software I2c solution available (already in the main fabfile) that should be compatible. I'm yet to determine compatibility.

## Links

- https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/overview - learning material.

## Adafruit implementation

Adafruit has a Raspberry Pi implementation for this board using UART instead of i2c. There may be a little work to find an i2c implementation that is compatible,.

## Other implementation

https://github.com/ghirlekar/bno055-python-i2c