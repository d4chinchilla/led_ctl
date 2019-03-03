# Based on example by Adafruit and using Adafruit libraries
 
# _____________________________________________________________________________
# Setup
#
# Import libraries
# Setup LEDs for Adafruit library
# Setup button and declare as pull up input
# Setup memory for remembering id, time and button state between loops
# Declare the fanout round the LED ring
# _____________________________________________________________________________

# imports
import time
import board
import neopixel
import json
import digitalio
from math import pi

# LED setup
pixel_pin = board.D18
num_pixels = 46
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1,
                           auto_write=False, pixel_order=ORDER)

# Button setup
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Declare memory between angles
last_id = 0
last_ms = 0
last_button = 0

# Declare fanout
fan_out = 3

# _____________________________________________________________________________
# Sign function
#
# This outputs only the sign of a number ignoring the value
# Possible outputs are 1 and -1
# _____________________________________________________________________________
def sign(num):
    if num <= 0:
        return -1
    else:
        return 1

# _____________________________________________________________________________
# LED ring code
#
# Calculates LED RGB values based on angle and amplitude
# Fades out as it goes round the ring up to the fanout value
# _____________________________________________________________________________
def led_ring(angle, amplitude):
    
    # Translate angle to LED number
    ring_pos = round((angle * num_pixels) / (2 * pi))
    
    # Offset from Led number found above
    ring_offset = ((angle * num_pixels) / (2 * pi)) - ring_pos
    
    # For loop stepping through fan_out
    for n in range(1 - fan_out, 1 + fan_out):
        
        # Calculate LED index based on angle
        index = ring_pos + (n * sign(ring_offset)) + (num_pixels *
                cmp(-ring_pos - (n * sign(ring_offset)), 0))
        
        # Extract current value of LED in question
        pixel = list(pixels[index])

        # Calculate RGB values for LEDs incorporating:
        # past value, amplitude and angle
        pixels[index] = (( min(255, pixel[0] + round(amplitude * 255 *
                           max(0, ((2 * amplitude) - 1)) * (fan_out - abs(n) +
                           (abs(ring_offset) * sign(n)) ) / fan_out )),
                           
                           min(255, pixel[1] + round(amplitude * 255 *
                           (1 - abs((2 * amplitude) - 1)) * (fan_out - abs(n) +
                           (abs(ring_offset) * sign(n)) ) / fan_out )),
                           
                           min(255, pixel[2] + round(amplitude * 255 *
                           max(0, ((-2 * amplitude) + 1)) * (fan_out - abs(n) +
                           (abs(ring_offset) * sign(n)) ) / fan_out )) ))
    
    # Display LED values calculated
    pixels.show()

# _____________________________________________________________________________
# Main loop
# Imports angle and amplitude value from json file, and triggers LED ring code
# Fades the LED values by 1/3 each loop
# Reads button value
# Sends a calibrate command if short button press
# Sends a reset command if long button press
# _____________________________________________________________________________
while True:
    
    # Fade all LEDs out by 1/3 each time
    for i in range(0, num_pixels):
        
        # Convert from tuple to list for current LED
        pixel = list(pixels[i])
        if pixel[0] > 0:
            pixel[0] -= max(1, round(pixel[0]/3))
        if pixel[1] > 0:
            pixel[1] -= max(1, round(pixel[1]/3))
        if pixel[2] > 0:
            pixel[2] -= max(1, round(pixel[2]/3))
            
        # Convert back from list to tuple for current LED
        pixels[i] = tuple(pixel)
        
        # Display LED values calculated
        pixels.show()

    # Open Json file and read id, angle and amplitude
    with open('/tmp/chinchilla-backend.json', 'r') as json_file:
        for line in json_file.readlines():
            object = json.loads(line)
            id = object['id']
            angle = object['angle']
            amplitude = object['amplitude']
            
            # Check id has increased (don't repeat same sound)
            if id > last_id:
                
                # Call LED ring code
                led_ring(angle, amplitude)
                
                # Update last id memory
                last_id = id
    
    # Get current time in milliseconds
    now_ms = int(time.time() * 1000)
    
    # Get current button value
    button_value = not button.value
    
    # Open file, write command and close
    f = open('/tmp/chinchilla-led-ctl', 'w')
    if (button_value and last_button == 0):
        last_ms = now_ms
    if (button_value and now_ms > last_ms + 2000 and last_button == 1):
        f.write('reset')
    elif (button_value and now_ms > last_ms + 50 and last_button == 1):
        f.write('calibrate')
    f.close()
    
    # Update last button memory
    last_button = button_value
