# Based on example by adafruit

import time
import board
import neopixel
import json

# Neopixel setup
pixel_pin = board.D18
num_pixels = 60
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

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
    pixles[ring_pos + (-2 * offset_sign)] = (( (amplitude * max(0, ((2 * amplitude) - 1)) * (1 - ring_offset) / 3 ),
                                               (amplitude * (1 - abs((2 * amplitude) - 1)) * (1 - ring_offset) / 3 ),
                                               (amplitude * max(0, ((-2 * amplitude) + 1)) * (1 - ring_offset) / 3 ) ))
    pixles[ring_pos + (-1 * offset_sign)] = (( (amplitude * max(0, ((2 * amplitude) - 1)) * (2 - ring_offset) / 3 ),
                                               (amplitude * (1 - abs((2 * amplitude) - 1)) * (2 - ring_offset) / 3 ),
                                               (amplitude * max(0, ((-2 * amplitude) + 1)) * (2 - ring_offset) / 3 ) ))
    pixels[ring_pos + ( 0 * offset_sign)] = (( (amplitude * max(0, ((2 * amplitude) - 1)) * (3 - ring_offset) / 3 ),
                                               (amplitude * (1 - abs((2 * amplitude) - 1)) * (3 - ring_offset) / 3 ),
                                               (amplitude * max(0, ((-2 * amplitude) + 1)) * (3 - ring_offset) / 3 ) ))
    pixels[ring_pos + ( 1 * offset_sign)] = (( (amplitude * max(0, ((2 * amplitude) - 1)) * (2 + ring_offset) / 3 ),
                                               (amplitude * (1 - abs((2 * amplitude) - 1)) * (2 + ring_offset) / 3 ),
                                               (amplitude * max(0, ((-2 * amplitude) + 1)) * (2 + ring_offset) / 3 ) ))
    pixles[ring_pos + ( 2 * offset_sign)] = (( (amplitude * max(0, ((2 * amplitude) - 1)) * (1 + ring_offset) / 3 ),
                                               (amplitude * (1 - abs((2 * amplitude) - 1)) * (1 + ring_offset) / 3 ),
                                               (amplitude * max(0, ((-2 * amplitude) + 1)) * (1 + ring_offset) / 3 ) ))
    pixles[ring_pos + ( 3 * offset_sign)] = (( (amplitude * max(0, ((2 * amplitude) - 1)) * ring_offset / 3 ),
                                               (amplitude * (1 - abs((2 * amplitude) - 1)) * ring_offset / 3 ),
                                               (amplitude * max(0, ((-2 * amplitude) + 1)) * ring_offset / 3 ) ))
    pixels.show()

# Main loop
while True:
    for i in range(0, num_pixels):
        if pixels[i] > 0:
            pixels[i] = pixels[i] - 1
    
    with open('/tmp/chinchilla-backend.json', 'r') as json_file:
        for line in json_file.readlines():
            object = json.loads(line)
            var id = object.id
            var angle = object.angle
            var amplitude = object.amplitude
                
            if id > last_id:
                led_ring(angle, amplitude)
                last_id = id
            
            time.sleep(0.002)
