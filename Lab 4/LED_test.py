from __future__ import print_function
import qwiic_led_stick
import time
import sys

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 1")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the sytsem. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")
    
    my_stick.set_all_LED_brightness(15)

    while True:
        
        # Turn on all the LEDs to white
        my_stick.set_all_LED_color(50, 50, 50)
        time.sleep(1)
        # Turn off all LEDs
        my_stick.LED_off()
        time.sleep(1)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)