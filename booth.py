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

WIDTH, HEIGHT = 640, 480

def printMugshot(image):
    """ Prepare and print a captured image
    on the thermal printer
    """

    nowname = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = "%s.jpg" % nowname
    pygame.image.save(image, filename)
    

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera('/dev/video1', (WIDTH, HEIGHT))
cam.start()
image = cam.get_image()

screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption("pyGame Camera View")

while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONUP :
            printMugshot(image)
    
    # draw frame
    screen.blit(image, (0,0))
    pygame.display.flip()
    # grab next frame    
    image = cam.get_image()
