# SPDX-FileCopyrightText: Copyright (c) 2021 David Glaude
#
# SPDX-License-Identifier: Unlicense
import board
from time import sleep
import adafruit_st25dv16
from adafruit_msa3xx import MSA311
import subprocess
import cryptography

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

i2c = board.I2C()
eeprom = adafruit_st25dv16.EEPROM_I2C(i2c)
msa = MSA311(i2c)

def curr_accel():
    max_value = 0
    for i, z in enumerate(msa.acceleration):
        value = abs(z)
        if value > abs(max_value):
            max_value = msa.acceleration[i]
    return max_value

def curr_temp():
    cmd = "cat /sys/class/thermal/thermal_zone0/temp"
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    return float(Temp) / 1000

def write_to_nfc(header, mess): 
    head = header

    l=len(mess)

    buf = bytearray ([0xe1, 0x40, 0x40, 0x05, 0x03, 0x00, 0xd1, 0x01, 0x00, 0x00])
    buf[5] = (l+5)
    buf[8] = (l+1)
    eeprom[0:len(buf)]=buf
    eeprom[len(buf)]=head
    k=len(buf)+1
    eeprom[k:k+l]=bytearray(mess, encoding='utf-8')
    eeprom[k+l]=0xfe

    print("Writing to NFC Chip")


for i in range(0, 6):
    j = i * 16
    hex_string = ":".join("%02x" % b for b in eeprom[j:j+15])
    print(j, "> ", hex_string, "> ", eeprom[j:j+15])

max_accel = 0
max_temp = 0
while True:
    
    max_accel = max(curr_accel(), max_accel)
    max_temp = max(curr_temp(), max_temp)
    opened= 0

    header = 0x00
    message=f'Max accelaration: {max_accel} - Max Temperature: {max_temp}'
    write_to_nfc(header, message)

    sleep(2)