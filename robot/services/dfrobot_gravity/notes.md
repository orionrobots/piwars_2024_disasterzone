# Notes on Gravity Expansion Hat

This is for driving a robot using the [DFRobot Gravity Expansion hat](https://thepihut.com/products/gravity-io-expansion-hat-for-raspberry-pi-4?variant=38140465316035&currency=GBP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic), plus an external motor driver board connected to it's pins.

Like the other motor modules in this project, it will follow the GPIOZero robot interface.  

- [Product wiki](https://wiki.dfrobot.com/IO%20Expansion%20HAT%20for%20Raspberry%20Pi%20%20SKU%3A%20%20DFR0566)
- [Expansion hat](https://thepihut.com/products/gravity-io-expansion-hat-for-raspberry-pi-4)
- [Motor driver](https://thepihut.com/products/gravity-2x-1-2a-dc-motor-driver-tb6612fng) - This is just a TB6612fng with headers

## Setup

The wiring is as follows, using the gravity modular wires:

| Motor Driver | Gravity Hat | Raspberry Pi |
| ------------ | ----------- | ------------ |
| PWM1         | PWM0        | I2C          |
| DIR1         | D0          | GPIO 0       |
| PWM2         | PWM1        | I2C          |
| DIR2         | D1          | GPIO 1       |

This allows the motor board to use only 2 PWM outputs, freeing up a further 2 for use with servo motors.

## Usage

We should be able to see the board on I2C when we power up the Pi.

For example: `fab -e -H danny@learnrob3.local show-i2c-devices`
