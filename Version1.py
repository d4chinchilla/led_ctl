# Based on example by Adafruit and using Adafruit libraries
 
# _____________________________________________________________________________
# Setup
# _____________________________________________________________________________

import time
import board
import neopixel
import json
import digitalio

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

# Define pi
pi = 3.14159265359

# Declare memory
last_id = 0
now_ms = 0
last_ms = 0
button_value = 0
last_button = 0

# Declare LED indices
index_2 = 0
index_1 = 0
index0 = 0
index1 = 0
index2 = 0
index3 = 0

# Declare position and offset on LED ring and offset signedness
ring_pos = 0
ring_offset = 0
offset_sign = 0

# _____________________________________________________________________________
# LED ring code
# _____________________________________________________________________________
def led_ring(angle, amplitude):
	
	# Translate angle to LED number
    ring_pos = round((angle * num_pixels) / (2 * pi))
    ring_offset = ((angle * num_pixels) / (2 * pi)) - ring_pos

    if ring_offset < 0:
        offset_sign = -1
    elif ring_offset > 0:
        offset_sign = 1
    else:
        offset_sign = 0

    ring_offset = abs(ring_offset)
    
    # Work out LED values
    if (ring_pos + (-2 * offset_sign)) < 0:
        index_2 = ring_pos + (-2 * offset_sign) + num_pixels
    elif (ring_pos + (-2 * offset_sign)) >= num_pixels:
        index_2 = ring_pos + (-2 * offset_sign) - num_pixels)
    else:
        index_2 = ring_pos + (-2 * offset_sign)
    
    pixel = list(pixels[index_2])

    pixels[index_2] = (( min(255, pixel[0] + round(amplitude * 255 *
        max(0, ((2 * amplitude) - 1)) * (1 - ring_offset) / 3 )),
                         min(255, pixel[1] + round(amplitude * 255 *
        (1 - abs((2 * amplitude) - 1)) * (1 - ring_offset) / 3 )),
                         min(255, pixel[2] + round(amplitude * 255 *
        max(0, ((-2 * amplitude) + 1)) * (1 - ring_offset) / 3 )) ))
    
    
    if (ring_pos - offset_sign) < 0:
        index_1 = ring_pos - offset_sign + num_pixels
    elif (ring_pos - offset_sign) >= num_pixels:
        index_1 = ring_pos - offset_sign - num_pixels)
    else:
        index_1 = ring_pos - offset_sign
    
    pixel = list(pixels[index_1])
    
    pixels[index_1] = (( min(255, pixel[0] + round(amplitude * 255 *
        max(0, ((2 * amplitude) - 1)) * (2 - ring_offset) / 3 )),
                         min(255, pixel[1] + round(amplitude * 255 *
        (1 - abs((2 * amplitude) - 1)) * (2 - ring_offset) / 3 )),
                         min(255, pixel[2] + round(amplitude * 255 *
        max(0, ((-2 * amplitude) + 1)) * (2 - ring_offset) / 3 )) ))
    
    
    if ring_pos < 0:
        index0 = ring_pos + num_pixels
    elif ring_pos >= num_pixels:
        index0 = ring_pos - num_pixels
    else:
        index0 = ring_pos
    
    pixel = list(pixels[index0])
    
    pixels[index0] = (( min(255, pixel[0] + round(amplitude * 255 *
        max(0, ((2 * amplitude) - 1)) * (3 - ring_offset) / 3 )),
                        min(255, pixel[1] + round(amplitude * 255 *
        (1 - abs((2 * amplitude) - 1)) * (3 - ring_offset) / 3 )),
                        min(255, pixel[2] + round(amplitude * 255 *
        max(0, ((-2 * amplitude) + 1)) * (3 - ring_offset) / 3 )) ))
    
    
    if (ring_pos + offset_sign) < 0:
        index1 = ring_pos + offset_sign + num_pixels
    elif (ring_pos + offset_sign) >= num_pixels:
        index1 = ring_pos + offset_sign - num_pixels)
    else:
        index1 = ring_pos + offset_sign
    
    pixel = list(pixels[index1])
    
    pixels[index1] = (( min(255, pixel[0] + round(amplitude * 255 *
        max(0, ((2 * amplitude) - 1)) * (2 + ring_offset) / 3 )),
                        min(255, pixel[1] + round(amplitude * 255 *
        (1 - abs((2 * amplitude) - 1)) * (2 + ring_offset) / 3 )),
                        min(255, pixel[2] + round(amplitude * 255 *
        max(0, ((-2 * amplitude) + 1)) * (2 + ring_offset) / 3 )) ))
    
    
    if (ring_pos + (2 * offset_sign)) < 0:
        index2 = ring_pos + (2 * offset_sign) + num_pixels
    elif (ring_pos + (2 * offset_sign)) >= num_pixels:
        index2 = ring_pos + (2 * offset_sign) - num_pixels)
    else:
        index2 = ring_pos + (2 * offset_sign)
    
    pixel = list(pixels[index2])
    
    pixels[index2] = (( min(255, pixel[0] + round(amplitude * 255 *
        max(0, ((2 * amplitude) - 1)) * (1 + ring_offset) / 3 )),
                        min(255, pixel[1] + round(amplitude * 255 *
        (1 - abs((2 * amplitude) - 1)) * (1 + ring_offset) / 3 )),
                        min(255, pixel[2] + round(amplitude * 255 *
        max(0, ((-2 * amplitude) + 1)) * (1 + ring_offset) / 3 )) ))
    
    
    if (ring_pos + (3 * offset_sign)) < 0:
        index3 = ring_pos + (3 * offset_sign) + num_pixels
    elif (ring_pos + (3 * offset_sign)) >= num_pixels:
        index3 = ring_pos + (3 * offset_sign) - num_pixels)
    else:
        index3 = ring_pos + (3 * offset_sign)
    
    pixel = list(pixels[index3])
    
    pixels[index3] = (( min(255, pixel[0] + round(amplitude * 255 *
        max(0, ((2 * amplitude) - 1)) * ring_offset / 3 )),
                        min(255, pixel[1] + round(amplitude * 255 *
        (1 - abs((2 * amplitude) - 1)) * ring_offset / 3 )),
                        min(255, pixel[2] + round(amplitude * 255 *
        max(0, ((-2 * amplitude) + 1)) * ring_offset / 3 )) ))
    
    pixels.show()

# _____________________________________________________________________________
# Main loop
# _____________________________________________________________________________
while True:
	
	# Fade LEDs out
    for i in range(0, num_pixels):
        pixel = list(pixels[i])
        if pixel[0] > 0:
            pixel[0] -= max(1, round(pixel[0]/3))
        if pixel[1] > 0:
            pixel[1] -= max(1, round(pixel[1]/3))
        if pixel[2] > 0:
            pixel[2] -= max(1, round(pixel[2]/3))
        pixels[i] = tuple(pixel)
        pixels.show()

    # Open Json file and trigger LED code
    with open('/tmp/chinchilla-backend.json', 'r') as json_file:
        for line in json_file.readlines():
            object = json.loads(line)
            id = object['id']
            angle = object['angle']
            amplitude = object['amplitude']
            
            if id > last_id:
                led_ring(angle, amplitude)
                last_id = id
    
    # Button code
    now_ms = int(time.time() * 1000)
    button_value = not button.value
    f = open('/tmp/chinchilla-led-ctl', 'w')
    if (button_value and last_button = 0):
        last_ms = now_ms
    if (button_value and now_ms > last_ms + 2000 and last_button = 1):
        f.write('reset')
    elif (button_value and now_ms > last_ms + 50 and last_button = 1):
        f.write('calibrate')
    f.close()
    last_button = button_value
