import time
import board
from adafruit_msa3xx import MSA311, TapDuration

i2c = board.I2C()  # uses board.SCL and board.SDA
msa = MSA311(i2c)

while True:
    print("%f %f %f" % msa.acceleration)
    time.sleep(0.5)