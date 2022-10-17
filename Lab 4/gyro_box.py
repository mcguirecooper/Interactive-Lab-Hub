import time
import board
import busio

import adafruit_mpr121
from adafruit_msa3xx import MSA311
import qwiic_led_stick

import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 270

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 80)

y = -2
draw.text((0, y), 'NO', font=font1, fill="#FF0000")
y += font1.getsize('NO')[1] + 15
draw.text((0, y), 'ORIENTATION', font=font1, fill="#FF0000")
y += font1.getsize('ORIENTATION')[1] + 15
draw.text((0, y), 'ASSIGNED', font=font1, fill="#FF0000")

# Display image.
disp.image(image, rotation)

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)
msa = MSA311(i2c)
my_stick = qwiic_led_stick.QwiicLEDStick()
my_stick.set_all_LED_brightness(15)
my_stick.set_all_LED_color(0, 0, 255)
time.sleep(1)
my_stick.LED_off()

asking_for_orientation = False

orientation = 0
# 0 = unassigned, 1 = top, 2 = bottom, 3 = left, 4 = right, 5 = front, 6 = back

def curr_accel_orient():
    orient = 1
    max_index = -1
    max_value = 0
    for i, z in enumerate(msa.acceleration):
        value = abs(z)
        if value > abs(max_value):
            max_index = i
            max_value = msa.acceleration[i]

    if max_index == 0:
        if max_value > 0:
            orient = 6
        else: orient = 5
    elif max_index == 1:
        if max_value > 0:
            orient = 4
        else: orient = 3
    elif max_index == 2:
        if max_value > 0:
            orient = 1
        else: orient = 2 
    print(max_index, max_value, orient)
    return orient

def blink_green():
    my_stick.set_all_LED_brightness(15)
    my_stick.set_all_LED_color(0, 255, 0)
    time.sleep(1)
    my_stick.LED_off()

def blink_red():
    my_stick.set_all_LED_brightness(15)
    my_stick.set_all_LED_color(255, 0, 0)
    time.sleep(1)
    my_stick.LED_off()
    time.sleep(1)


#print("%f %f %f" % msa.acceleration)
## INTERACTION BEGINS HERE

while True:
    if not buttonB.value or not buttonA.value: 
        print('Start buttons pressed')
        asking_for_orientation = True

        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image, rotation)
        y = 25
        draw.text((0, y), 'CHOOSE', font=font1, fill="#FF0000")
        y += font1.getsize('CHOOSE')[1] + 15
        draw.text((0, y), 'ORIENTATION', font=font1, fill="#FF0000")
        disp.image(image, rotation)

        break
    # for i in range(12):
    #     if mpr121[i].value:
    #         print(f"Package face {i-5} touched!")
    time.sleep(0.5)

while asking_for_orientation: 
    if mpr121[6].value:
        time.sleep(0.5)
        if mpr121[6].value:
            orientation = 4
            blink_green()
            break
    elif mpr121[7].value:
        time.sleep(0.5)
        if mpr121[7].value:
            orientation = 6
            blink_green()
            break
    elif mpr121[8].value:
        time.sleep(0.5)
        if mpr121[8].value:
            orientation = 3
            blink_green()
            break
    elif mpr121[9].value:
        time.sleep(0.5)
        if mpr121[9].value:
            orientation = 5
            blink_green()
            break
    elif mpr121[0].value:
        time.sleep(0.5)
        if mpr121[0].value:
            orientation = 1
            blink_green()
            break

while orientation != 0:
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, rotation)

    arrows = ['N','⊚','⊕','⇐','⇒','⇓','⇑']

    x = width/2
    y = -2
    draw.text((x, y), 'THIS', font=font2, fill="#FFFFFF")
    y += font2.getsize('THIS')[1]
    draw.text((x, y), 'SIDE', font=font2, fill="#FFFFFF")
    y += font2.getsize('SIDE')[1]
    draw.text((x, y), 'UP', font=font2, fill="#FFFFFF")
    draw.text((20, height/8), arrows[orientation], font=font3, fill="#FFFFFF")
    disp.image(image, rotation)

    if curr_accel_orient() != orientation:
        blink_red()
    
    time.sleep(1)
    


