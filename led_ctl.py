# Based on example by Adafruit and using Adafruit libraries

# imports
import time
import board
import neopixel
import json
import digitalio
import ast
from math import pi

# Definitions
FAN_OUT = 3
NUM_PIXELS = 46

# _____________________________________________________________________________
# Setup
#
# Setup LEDs for Adafruit library
# Setup button and declare as pull up input
# Setup memory for remembering id, time and button state between loops
# _____________________________________________________________________________

# LED setup
pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=1,
                               auto_write=False, pixel_order=ORDER)

# Button setup
button = digitalio.DigitalInOut(board.D23)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Declare memory between angles
last_id = 0
last_ms = 0

# _____________________________________________________________________________
# Loading animation on LEDs
# _____________________________________________________________________________
def load_screen():

    # Clear all LEDs
    for n in range(0,NUM_PIXELS):
        pixels[n] = ((0, 0, 0))
    pixels.show()

    # Make first and last LED white
    pixels[0] = ((255, 255, 255))
    pixels[NUM_PIXELS - 1] = ((255, 255, 255))

    # Display LED values calculated
    pixels.show()

    # Send white LED lit up round ring
    for n in range(1, int(NUM_PIXELS / 2)):
        time.sleep(0.1)

        pixels[n - 1] = ((0, 0, 0))
        pixels[n] = ((255, 255, 255))

        pixels[NUM_PIXELS - n] = ((0, 0, 0))
        pixels[NUM_PIXELS -1 - n] = ((255, 255, 255))

        # Display LED values calculated
        pixels.show()

    # Clear all LEDs
    for n in range(0,NUM_PIXELS):
        pixels[n] = ((0, 0, 0))
    pixels.show()

    # Light up all LEDs in sequence with colours that range from orange to purple
    for n in range(int(NUM_PIXELS / 2) - 1, -1, -1):
        time.sleep(0.1)
        pixels[n] = ((round(n * 255 / (int(NUM_PIXELS / 2) - 1)), n, round(255 - (n * 255 / (int(NUM_PIXELS / 2) - 1))) ))
        pixels[NUM_PIXELS -1 - n] = ((round(n * 255 / (int(NUM_PIXELS / 2) - 1)), n, round(255 - (n * 255 / (int(NUM_PIXELS / 2) - 1))) ))

        # Display LED values calculated
        pixels.show()

    time.sleep(1)

    # Clear all LEDs
    for n in range(0,NUM_PIXELS):
        pixels[n] = ((0, 0, 0))
    pixels.show()

# _____________________________________________________________________________
# Calibration animation
# _____________________________________________________________________________
def calibrate():
    # Clear all LEDs
    for n in range(0,NUM_PIXELS):
        pixels[n] = ((0, 0, 0))
    pixels.show()

    # Make first LED white
    pixels[0] = ((255, 255, 255))

    # Display LED values calculated
    pixels.show()

    # Send white LED lit up round ring
    for n in range(1, NUM_PIXELS):
        time.sleep(0.1)

        pixels[n - 1] = ((0, 0, 0))
        pixels[n] = ((255, 255, 255))

        # Display LED values calculated
        pixels.show()

    # Clear all LEDs
    for n in range(0,NUM_PIXELS):
        pixels[n] = ((0, 0, 0))
    pixels.show()

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
def led_ring(angle, amplitude, freq):

    # Translate angle to LED number
    ring_pos = round((angle * NUM_PIXELS) / (2 * pi))

    # Offset from Led number found above
    ring_offset = ((angle * NUM_PIXELS) / (2 * pi)) - ring_pos

    # For loop stepping through FAN_OUT
    for n in range(1 - FAN_OUT, 1 + FAN_OUT):

        # Calculate LED index based on angle
        index = ring_pos + (n * sign(ring_offset)) + (NUM_PIXELS *
                sign(-ring_pos - (n * sign(ring_offset))))

        # Extract current value of LED in question
        pixel = list(pixels[index])

        # Calculate RGB values for LEDs incorporating:
        # past value, amplitude and angle

        pixels[index] = (( max(0, min(255, pixel[0] + round(amplitude * 255 *
                           max(0, ((freq / 500) - 1)) * (FAN_OUT - abs(n) +
                           (abs(ring_offset) * sign(n)) ) / FAN_OUT ))),

                           max(0, min(255, pixel[1] + round(amplitude * 255 *
                           (1 - abs((freq / 500) - 1)) * (FAN_OUT - abs(n) +
                           (abs(ring_offset) * sign(n)) ) / FAN_OUT ))),

                           max(0, min(255, pixel[2] + round(amplitude * 255 *
                           max(0, ((-freq / 500) + 1)) * (FAN_OUT - abs(n) +
                           (abs(ring_offset) * sign(n)) ) / FAN_OUT )) )))

    # Display LED values calculated
    pixels.show()

# _____________________________________________________________________________
# Main Code
#
# Call setup
# Imports angle and amplitude value from json file, and triggers LED ring code
# Fades the LED values by 1/3 each loop
# Reads button value
# Sends a calibrate command if short button press
# Sends a reset command if long button press
# _____________________________________________________________________________

load_screen()

while True:

    # Fade all LEDs out by 1/3 each time
    for i in range(0, NUM_PIXELS):

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
    with open('/tmp/chinchilla-sounds', 'r') as json_file:
        for line in json_file.readlines():
            object = json.loads(line)
            id = object['id']
            angle = object['angle']
            amplitude = object['amplitude'] / 2000000.0

    # Import FFT data
    try:
        fft = ast.literal_eval(open('/tmp/chinchilla-fft', 'r').read())
    except:
        fft = None
    
    # Check for frequency with largest amplitude and use that
    if fft != None:
        largest_amp = 0
        for currfreq, ampl in fft['fft'].items():
            if ampl > largest_amp:
                freq = currfreq
                largest_amp = ampl
    
    # Or default frequency of 500
    else:
        freq = 500
        
    # Check id has increased (don't repeat same sound)
    if id > last_id:

        # Call LED ring code
        led_ring(angle, amplitude, freq)

        # Update last id memory
        last_id = id

    # Get current time in milliseconds
    now_ms = int(time.time() * 1000)

    # Get current button value
    button_value = not button.value

    # Open file, write command and close if button press is greater than 50ms (debounce)
    f = open('/tmp/backend-ctl', 'w')
    if (not button_value):
        last_ms = now_ms
    if (button_value and now_ms > last_ms + 50):
        f.write('calibrate')
    f.close()
    
    # Trigger calibration animation
    if (button_value and now_ms > last_ms + 50):
        calibrate()

