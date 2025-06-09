# Baddie and BaddieMgr classes JSP

import pygame
import pygwidgets
import random
from src.Constants import *

# Baddie class
class Baddie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    # Load the image only once
    BADDIE_IMAGE = pygame.image.load(f'{RESOURCES_PATH}/images/fGrade.png')

    def __init__(self, window):
        self.window = window
        # Create the image object
        size = random.randrange(Baddie.MIN_SIZE, Baddie.MAX_SIZE + 1)
        self.x = random.randrange(0, WINDOW_WIDTH - size)
        self.y = 0 - size  # start above the window
        self.image = pygwidgets.Image(self.window, (self.x, self.y), Baddie.BADDIE_IMAGE)

        # Scale it
        percent = (size * 100) / Baddie.MAX_SIZE
        self.image.scale(percent, False)
        self.speed = random.randrange(Baddie.MIN_SPEED, Baddie.MAX_SPEED + 1)

    def update(self, scale=1.0):  # move the Baddie down
        self.y += self.speed * scale
        self.image.setLoc((self.x, self.y))
        if self.y > GAME_HEIGHT:
            return True  # needs to be deleted
        else:
            return False  # stays in the window

    def draw(self):
        self.image.draw()

    def collide(self, playerRect):
        return self.image.overlaps(playerRect)

# BaddieMgr class
class BaddieMgr():
    ADD_NEW_BADDIE_RATE = 8  # how often to add a new Baddie

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # called when starting a new game
        self.baddiesList = []
        self.nFramesTilNextBaddie = BaddieMgr.ADD_NEW_BADDIE_RATE

    def update(self, scale=1.0):
        nBaddiesRemoved = 0
        baddiesListCopy = self.baddiesList.copy()
        for oBaddie in baddiesListCopy:
            deleteMe = oBaddie.update(scale)
            if deleteMe:
                self.baddiesList.remove(oBaddie)
                nBaddiesRemoved += 1

        if scale > 0:
            self.nFramesTilNextBaddie -= 1
            if self.nFramesTilNextBaddie <= 0:
                oBaddie = Baddie(self.window)
                self.baddiesList.append(oBaddie)
                self.nFramesTilNextBaddie = BaddieMgr.ADD_NEW_BADDIE_RATE

        return nBaddiesRemoved

    def draw(self):
        for oBaddie in self.baddiesList:
            oBaddie.draw()

    def hasPlayerHitBaddie(self, playerRect):
        for oBaddie in self.baddiesList:
            if oBaddie.collide(playerRect):
                return True
        return False