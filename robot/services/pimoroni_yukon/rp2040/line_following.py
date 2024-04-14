from machine import I2C
import struct


i2c = I2C(0)
i2c.scan()


class LineFollower:
    def __init__(self, i2c_address=0x11, i2c=None) -> None:
        if i2c is None:
            self.i2c = I2C(0)
        else:
            self.i2c = i2c
        self.i2c_address = i2c_address

    def get_values(self):
        return struct.unpack(
            ">HHHHH",
            i2c.readfrom(
                self.i2c_address, 10)
        )

    def get_differences(self):
        values = self.get_values()
        return (
            abs(values[0] - values[1]),
            abs(values[1] - values[2]),
            abs(values[2] - values[3]),
            abs(values[3] - values[4])
        )
