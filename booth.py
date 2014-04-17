#!/usr/bin/env python
"""
** Monobooth **

A thermal printer photobooth

"""
import sys
import pygame
import pygame.camera
from pygame.locals import *
from datetime import datetime
from escpos import *
import Image
import random

WIDTH, HEIGHT = 640, 480
videodev = '/dev/video1'

# use lsusb -v
Epson = printer.Usb(0x0483, 0x5740, 1, 0x81, 0x03)

def printMugshot(image):
    """ Prepare and print a captured image
    on the thermal printer
    """

    nowname = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = "%s.jpg" % nowname
    pygame.image.save(image, filename)  # save file just to have it

    pil_string_image = pygame.image.tostring(image, "RGB", False)
    pil_image = Image.fromstring("RGB",(WIDTH, HEIGHT),pil_string_image)

    # size_img = pil_image.resize((336, 252), Image.ANTIALIAS)
    margin = (WIDTH - HEIGHT) / 2
    size_img = pil_image.crop((MARGIN, 0, WIDTH-MARGIN, HEIGHT)).resize((120, 120), Image.ANTIALIAS)
    mono_img = size_img.convert('1')  # turn into monochrome in PIL

    img = mono_img
    filename2 = "%s-print.gif" %nowname
    img.save(filename2)

    Epson.set(align='center', type='b')
    Epson.text("> VIA MonoBooth <\n\n")
    Epson.set(align='left', type='normal')

    Epson.image(filename2)
    Epson.text(datetime.now().strftime("%Y-%m-%d %H:%M:%S\n\n"));

    Epson.text("Have a fun day!\n\n\n")

    Epson.cut()

## Start the booth
pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera(videodev, (WIDTH, HEIGHT))
cam.start()
image = cam.get_image()

screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption("MonoBooth")

while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.KEYDOWN :
            printMugshot(image)
    
    # draw frame
    screen.blit(image, (0,0))
    pygame.display.flip()
    # grab next frame    
    image = cam.get_image()
