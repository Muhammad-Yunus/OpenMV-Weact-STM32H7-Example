import sensor, image, lcd, pyb, time, os

# Init camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)

# Init LCD
lcd.init(type=2)

# Init GPIO
KEY = pyb.Pin('C13', pyb.Pin.IN, pyb.Pin.PULL_DOWN)
LED = pyb.LED(1)

while True:
    # Capture and save image
    img = sensor.snapshot()
    lcd.display(img)  # Display the image on the LCD
    if KEY.value() == 1:
        LED.on()
        filename = f"img_{time.ticks_ms()}.jpg"
        img.save(filename, quality=90)
        print(f"Saved image to: {filename}")
        time.sleep(1)
        LED.off()