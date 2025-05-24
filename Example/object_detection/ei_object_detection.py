# Edge Impulse - OpenMV FOMO Object Detection Example
#
# This work is licensed under the MIT license.
# Copyright (c) 2013-2024 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE

import sensor, image, time, tf, math, uos, gc, lcd, pyb

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)      # Set frame size to QQVGA
sensor.skip_frames(time=2000)          # Let the camera adjust.
lcd.init(type=2)                          # Initialize the LCD.
LED = pyb.LED(1)
net = None
labels = None
min_confidence = 0.5

x = 0
y = 0
w = 0
h = 0 
score = 0
index = 0

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

colors = [
    (0,   0,   0),
    (0, 128, 255),
    (255, 0, 128)
]

clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    for i, detection_list in enumerate(net.detect(img)): #, callback=fomo_post_process
        if i == 0: 
            if detection_list[i][4] == 1.0 :
                score = 0  # reset score for background class
            continue  # background class
        if len(detection_list) == 0: continue  # no detections for this class?
        LED.on()
        max_score = max(detection[4] for detection in detection_list)
        max_index = next(i for i, detection in enumerate(detection_list) if detection[4] == max_score) 

        detection = detection_list[max_index]
        x = max(detection[0] - 50, 0)
        y = max(detection[1] - 40, 0)
        w = detection[2] * 3
        h = detection[3] * 6
        score = detection[4]
        index = i
        print(f"{labels[i]} (x {x}\ty {y}\tw {w}\th {h}\tscore {score})")

    if score > 0 :
        img.draw_rectangle(x, y, w, h, color=colors[index])
        img.draw_rectangle(x, max(y-12, 0), w, 12, color=colors[index], fill=True)
        img.draw_string(x+2, max(y-10, 0), labels[index].upper(), color=(255,255,255), scale=1)

    img.draw_string(5, 80 - 12, f"{int(clock.fps())} FPS", color=(255,255,255), scale=1)
    lcd.display(img)
    LED.off()