import time
import sys
import board
import signal
from adafruit_msa3xx import MSA311
import qwiic_led_stick

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

User = 'Cooper'
topic = 'IDD/Falling/Users/' + User

my_stick = qwiic_led_stick.QwiicLEDStick()
if my_stick.begin() == False:
    print("\nThe Qwiic LED Stick isn't connected to the sytsem. Please check your connection", \
        file=sys.stderr)
print("LED Stick ready!")

def blink_LED():
    for n in range(20):
        # Turn on all the LEDs to red
        my_stick.set_all_LED_color(255, 0, 0)
        time.sleep(0.5)
        # Turn off all LEDs
        my_stick.LED_off()
        time.sleep(0.5)

# the wildcard means we subscribe to all subtopics of IDD
read_topic = 'IDD/Falling/Users/#'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(read_topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')

# this is the callback that gets called each time a message is recived
def on_message(client, userdata, msg):
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
    if msg.topic == 'IDD/Falling/Users/Cooper' or msg.topic == 'IDD/Falling/Users/Martin':
        blink_LED()

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#client.loop_forever()
client.loop_start()

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)

#when sigint happens, do the handler callback function
signal.signal(signal.SIGINT, handler)

fallen = False

while True:
    val = [abs(v) for v in msa.acceleration]
    #print(val)
    if max(val) > 9.8*1.5:
        fallen = True
    fall_message = User + ' has fallen. Send help!'
    if fallen:
        client.publish(topic, fall_message)

    time.sleep(0.1)
