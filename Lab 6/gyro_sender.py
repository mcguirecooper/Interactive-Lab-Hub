import time
import board
import busio
import adafruit_mpr121
from adafruit_msa3xx import MSA311

import paho.mqtt.client as mqtt
import uuid

i2c = board.I2C()  # uses board.SCL and board.SDA
msa = MSA311(i2c)

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/jacob/is /cool'

while True:
    val = str(msa.acceleration)
    print(val)
    client.publish(topic, val)
    time.sleep(0.25)
