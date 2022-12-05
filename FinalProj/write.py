# SPDX-FileCopyrightText: Copyright (c) 2021 David Glaude
#
# SPDX-License-Identifier: Unlicense
import board
from time import sleep
from datetime import datetime
import adafruit_st25dv16
from adafruit_msa3xx import MSA311
import subprocess
from ecdsa import SigningKey

i2c = board.I2C()
eeprom = adafruit_st25dv16.EEPROM_I2C(i2c)
msa = MSA311(i2c)

sk = SigningKey.generate()
vk = sk.verifying_key

print("""\
  _____              _                         _______                 _               
 |  __ \            | |                       |__   __|               | |              
 | |__) |__ _   ___ | | __ __ _   __ _   ___     | | _ __  __ _   ___ | | __ ___  _ __ 
 |  ___// _` | / __|| |/ // _` | / _` | / _ \    | || '__|/ _` | / __|| |/ // _ \| '__|
 | |   | (_| || (__ |   <| (_| || (_| ||  __/    | || |  | (_| || (__ |   <|  __/| |   
 |_|    \__,_| \___||_|\_\\__,_| \__, | \___|    |_||_|   \__,_| \___||_|\_\\___||_|   
                                  __/ |                                                
                                 |___/                                                 
""")
print("🔑 Verifying Key:")
print(vk.to_string().hex())

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
    print("Writing to NFC Chip:")
    print(mess)

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


max_accel = 0
max_temp = 0
while True:
    
    max_accel = round(max(curr_accel(), max_accel))
    max_temp = round(max(curr_temp(), max_temp))
    opened= 0

    header = 0x00
    
    report=f'Time: {datetime.now()} - Max acc: {max_accel} - Max Temp: {max_temp}'
    signature = sk.sign(report.encode('UTF-8'))

    msg = f"Report: [{report}] Signature {signature.hex()}"

    write_to_nfc(header, msg)

    sleep(2)