# Edge Impulse - OpenMV Image Classification Example
#
# This work is licensed under the MIT license.
# Copyright (c) 2013-2024 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE

import sensor, time, tf, uos, gc, lcd, pyb

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)      # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)          # Let the camera adjust.

lcd.init(type=2)                          # Initialize the LCD.

LED = pyb.LED(1)

net = None
labels = None
text_label = None
text_bg_color = (255, 255, 255) 
text_color = (0, 0, 0) 

# LCD dimensions
width = 160 
height = 80 

# Define banner height
banner_height = 15

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot()
    
    predictions = net.classify(img)
    confs = predictions[0][4]
    outputs = list(zip(labels, confs))

    # Only proceed if predictions are not equal and at least one is > 0.3
    if abs(confs[0] - confs[1]) > 0.001 and abs(confs[0] - confs[1]) != 0.0234375:
        LED.on()
        max_probability = max(confs)
        i = confs.index(max_probability)
        text_label = outputs[i][0] #"{}|{:.1f}".format(outputs[i][0], outputs[i][1]) 
        text_bg_color = (0, 128, 255) if i == 0 else (255, 0, 128)
        text_color = (255, 255, 255)
    else:
        LED.off()
        text_label = "EMPTY"
        text_bg_color = (255, 255, 255)
        text_color = (0, 0, 0) 

    text_width = len(text_label) * 16
    x_pos = (width - text_width) // 2
    y_pos = height - banner_height - 2
    img.draw_rectangle(0, height - banner_height, width, banner_height, color=text_bg_color, fill=True)
    img.draw_string(x_pos, y_pos, text_label, color=text_color, scale=2)

    lcd.display(img)
    print(text_label, " - ", confs[0], ",", confs[1], " - ", clock.fps(), "fps")