# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""
import math
from time import strftime, sleep
import digitalio
import board
from PIL import Image, ImageDraw
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

# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

back = Image.open('pixil-frame-1.jpg') 
back = back.rotate(180)
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Scale the image to the smaller screen dimension
image_ratio = back.width / back.height
screen_ratio = width / height
if screen_ratio < image_ratio:
    scaled_width = back.width * height // back.height
    scaled_height = height
else:
    scaled_width = width
    scaled_height = back.height * width // back.width
back = back.resize((scaled_width, scaled_height), Image.BICUBIC)

# Crop and center the image
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
back = back.crop((x, y, x + width, y + height))

#orbit ellipse shape
draw_orbit = ImageDraw.Draw(back)
draw_orbit.ellipse((12, 40, 112, 200), outline=(220,220,220))
draw_orbit.ellipse((3, 3, 132, 237), outline=(220,220,220))

#orbiting moon
ul_x, ul_y, lr_x, lr_y = 62, 190, 82, 210

#orbiting comet
ul_xc, ul_yc, lr_xc, lr_yc = 65, 234, 71, 240

theta = math.pi/2 #angle on orbit clock that is 12am
thetac = math.pi/2 #angle on comet clock that is 00:00
period_moon = 20 #period in seconds of lunar orbit
period_comet = 10 #period in seconds of comet orbit

button_add_period = 5 #seconds added to period comet or each button press

comet_started = False # if the comet timer is running

sleep_time = 0.20 # draw interval in sec
timer_left = period_comet # time left on comet timer

while True:
    
    draw_comet = ImageDraw.Draw(back)
    draw_comet.ellipse((ul_xc, ul_yc, lr_xc, lr_yc), fill=(0,0,0))
    draw_comet.ellipse((3, 3, 132, 237), outline=(220,220,220))
    draw_orbit.line((68, 230, 68, 240), fill=(0,255,0))
    draw_orbit.line((68, 0, 68, 10), fill=(0,255,0))

    if timer_left <= 0:
        comet_started = False
        draw_explosion = ImageDraw.Draw(back)
        #r = 35 #61-r, 120-r, 61+r, 120+r
        draw_explosion.ellipse((57, 60, 65, 180), fill=(255, 234, 0))
        draw_explosion.ellipse((57, 75, 65, 165), fill=(255, 128, 10))
        draw_explosion.ellipse((59, 90, 63, 150), fill=(255, 0, 0))

    if comet_started:
        ul_xc = int(65 * math.cos(thetac) + 65)
        ul_yc = int(117 * math.sin(thetac) + 117)
        lr_xc = ul_xc + 6
        lr_yc = ul_yc + 6

    draw_text = ImageDraw.Draw(back)
    draw_text.rectangle((0, 225, 30, 240), fill=(0,0,0))

    if not buttonB.value: 
        if not comet_started:  # b pressed and comet not started
            comet_started = True # set the comet to start
            print("B Button Pressed, Timer Started", comet_started)
        else:  # b pressed and comet currently going
            comet_started = False # set the comet to pause
            print("B Button Pressed, Timer Stopped", comet_started)
    if not buttonA.value and not comet_started:  # a pressed and comet not started
        period_comet += button_add_period  # add a number of seconds to the comet timer
        timer_left += button_add_period
        print("A Button Pressed, Added Time", period_comet)
        draw_text.text((5, 225), str(period_comet) + 's', fill=(249, 139, 136))

    draw_moon = ImageDraw.Draw(back)
    draw_moon.ellipse((ul_x, ul_y, lr_x, lr_y), fill=(0,0,0))
    draw_orbit.ellipse((12, 40, 112, 200), outline=(220,220,220))
    draw_orbit.ellipse((3, 3, 132, 237), outline=(220,220,220))
    draw_orbit.line((62, 195, 62, 205), fill=(255,0,0))
    draw_orbit.line((62, 35, 62, 45), fill=(255,0,0))

    ul_x = int(50 * math.cos(theta) + 52)
    ul_y = int(80 * math.sin(theta) + 110)
    lr_x = ul_x + 20
    lr_y = ul_y + 20
    
    draw_comet.ellipse((ul_xc, ul_yc, lr_xc, lr_yc), fill=(249, 139, 136))
    draw_moon.ellipse((ul_x, ul_y, lr_x, lr_y), fill=(220,220,220))
    disp.image(back)
    theta += 2 * math.pi/(period_moon / sleep_time)
    if comet_started: 
        thetac += 2 * math.pi/(period_comet / sleep_time)
        timer_left -= sleep_time
    sleep(sleep_time)