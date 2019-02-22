# Based on example by adafruit

import time
import board
import neopixel
import json

# Neopixel setup
pixel_pin = board.D18
num_pixels = 25
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

# Define pi
pi = 3.14159265359

# Declare Colour memory
red = 1
green = 0
blue = 0

# Declare position and offset on LED ring and offset signedness
ring_pos = 0
ring_offset = 0
offset_sign = 0

# Led ring code
def led_ring(angle, amplitude):
    ring_pos = round((angle * num_pixels) / (2 * pi))
    ring_offset = ((angle * num_pixels) / (2 * pi)) - ring_pos

    if ring_offset < 0:
        offset_sign = -1
    elif ring_offset > 0:
        offset_sign = 1
    else:
        offset_sign = 0

    ring_offset = abs(ring_offset)

    for i in range(0, 256):
        pixles[ring_pos + (-2 * offset_sign)] = (( (round(i * amplitude * red * (1 - ring_offset) / 3 )), (round(i * amplitude * green * (1 - ring_offset) / 3 )), (round(i * amplitude * blue * (1 - ring_offset) / 3 )) ))
        pixles[ring_pos + (-1 * offset_sign)] = (( (round(i * amplitude * red * (2 - ring_offset) / 3 )), (round(i * amplitude * green * (2 - ring_offset) / 3 )), (round(i * amplitude * blue * (2 - ring_offset) / 3 )) ))
        pixels[ring_pos + ( 0 * offset_sign)] = (( (round(i * amplitude * red * (3 - ring_offset) / 3 )), (round(i * amplitude * green * (3 - ring_offset) / 3 )), (round(i * amplitude * blue * (3 - ring_offset) / 3 )) ))
        pixels[ring_pos + ( 1 * offset_sign)] = (( (round(i * amplitude * red * (2 + ring_offset) / 3 )), (round(i * amplitude * green * (2 + ring_offset) / 3 )), (round(i * amplitude * blue * (2 + ring_offset) / 3 )) ))
        pixles[ring_pos + ( 2 * offset_sign)] = (( (round(i * amplitude * red * (1 + ring_offset) / 3 )), (round(i * amplitude * green * (1 + ring_offset) / 3 )), (round(i * amplitude * blue * (1 + ring_offset) / 3 )) ))
        pixles[ring_pos + ( 3 * offset_sign)] = (( (round(i * amplitude * red * (0 + ring_offset) / 3 )), (round(i * amplitude * green * (0 + ring_offset) / 3 )), (round(i * amplitude * blue * (0 + ring_offset) / 3 )) ))

        pixels.show()
        time.sleep(0.002)

        if red == 1:
            red = 0
            green = 1
            blue = 0
        elif green == 1:
            red = 0
            green = 0
            blue = 1
        else:
            red = 1
            green = 0
            blue = 0

# Main loop
while True:
        with open('/tmp/chinchilla-backend.json', 'r') as json_file:  
                data = json.load(json_file)
