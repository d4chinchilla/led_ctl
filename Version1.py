# Based on example by adafruit

import time
import board
import neopixel
import json

# Neopixel setup
pixel_pin = board.D18
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)

# Define pi
pi = 3.14159265359

# Declare id memory
last_id = 0

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
    if (ring_pos + (-2 * offset_sign)) > -1 and (ring_pos + (-2 * offset_sign)) < num_pixels:
        pixels[ring_pos + (-2 * offset_sign)] = (( round(amplitude * 255 * max(0, ((2 * amplitude) - 1)) * (1 - ring_offset) / 3 ),
                                                   round(amplitude * 255 * (1 - abs((2 * amplitude) - 1)) * (1 - ring_offset) / 3 ),
                                                   round(amplitude * 255 * max(0, ((-2 * amplitude) + 1)) * (1 - ring_offset) / 3 ) ))
    if (ring_pos + (-1 * offset_sign)) > -1 and (ring_pos + (-1 * offset_sign)) < num_pixels:
        pixels[ring_pos + (-1 * offset_sign)] = (( round(amplitude * 255 * max(0, ((2 * amplitude) - 1)) * (2 - ring_offset) / 3 ),
                                                   round(amplitude * 255 * (1 - abs((2 * amplitude) - 1)) * (2 - ring_offset) / 3 ),
                                                   round(amplitude * 255 * max(0, ((-2 * amplitude) + 1)) * (2 - ring_offset) / 3 ) ))
    if (ring_pos + ( 0 * offset_sign)) > -1 and (ring_pos + ( 0 * offset_sign)) < num_pixels:
        pixels[ring_pos + ( 0 * offset_sign)] = (( round(amplitude * 255 * max(0, ((2 * amplitude) - 1)) * (3 - ring_offset) / 3 ),
                                                   round(amplitude * 255 * (1 - abs((2 * amplitude) - 1)) * (3 - ring_offset) / 3 ),
                                                   round(amplitude * 255 * max(0, ((-2 * amplitude) + 1)) * (3 - ring_offset) / 3 ) ))
    if (ring_pos + ( 1 * offset_sign)) > -1 and (ring_pos + ( 1 * offset_sign)) < num_pixels:
        pixels[ring_pos + ( 1 * offset_sign)] = (( round(amplitude * 255 * max(0, ((2 * amplitude) - 1)) * (2 + ring_offset) / 3 ),
                                                   round(amplitude * 255 * (1 - abs((2 * amplitude) - 1)) * (2 + ring_offset) / 3 ),
                                                   round(amplitude * 255 * max(0, ((-2 * amplitude) + 1)) * (2 + ring_offset) / 3 ) ))
    if (ring_pos + ( 2 * offset_sign)) > -1 and (ring_pos + ( 2 * offset_sign)) < num_pixels:
        pixels[ring_pos + ( 2 * offset_sign)] = (( round(amplitude * 255 * max(0, ((2 * amplitude) - 1)) * (1 + ring_offset) / 3 ),
                                                   round(amplitude * 255 * (1 - abs((2 * amplitude) - 1)) * (1 + ring_offset) / 3 ),
                                                   round(amplitude * 255 * max(0, ((-2 * amplitude) + 1)) * (1 + ring_offset) / 3 ) ))
    if (ring_pos + ( 3 * offset_sign)) > -1 and (ring_pos + ( 3 * offset_sign)) < num_pixels:
        pixels[ring_pos + ( 3 * offset_sign)] = (( round(amplitude * 255 * max(0, ((2 * amplitude) - 1)) * ring_offset / 3 ),
                                                   round(amplitude * 255 * (1 - abs((2 * amplitude) - 1)) * ring_offset / 3 ),
                                                   round(amplitude * 255 * max(0, ((-2 * amplitude) + 1)) * ring_offset / 3 ) ))
    pixels.show()

# Main loop
while True:
    for i in range(0, num_pixels):
        pixel = list(pixels[i])
        if pixel[0] > 0:
            pixel[0] -= 1
        if pixel[1] > 0:
            pixel[1] -= 1
        if pixel[2] > 0:
            pixel[2] -= 1
        pixels[i] = tuple(pixel)
        pixels.show()

    with open('/tmp/chinchilla-backend.json', 'r') as json_file:
        for line in json_file.readlines():
            object = json.loads(line)
            id = object["id"]
            angle = object["angle"]
            amplitude = object["amplitude"]
            
            if id > last_id:
                led_ring(angle, amplitude)
                last_id = id
