import pygame as pyg
import math

class HealthBar(object):
    def __init__(self, screen, player, image_source, location):
        self.screen   = screen
        self.image    = pyg.image.load(image_source)
        self.location = location

        self.player = player
        
        self.top_left     = (location.x+7, location.y+11)
        self.top_right    = (self.top_left[0]+126, self.top_left[1])
        self.bottom_left  = (self.top_left[0], location.y+21)
        self.bottom_right = (self.top_right[0], self.bottom_left[1])
        self.height       = abs(self.top_left[1] - self.bottom_left[1])
        self.width        = abs(self.top_left[0] - self.top_right[0])
        self.color        = (255, 0, 0)
        
    def display(self):
        # first draw our image.
        self.screen.blit(self.image, (self.location.x, self.location.y))
        # build our rectangle but only if we still have health.
        if not self.player.is_dead():
            bar = pyg.Rect(self.top_left[0], 
                           self.top_left[1], 
                           self.width * self.player.health / self.player.full_health, # now we draw it only as long as health.
                           self.height)
                       
            # draw our rectangle on top of the image
            # 0 width means fill rectangle.
            pyg.draw.rect(self.screen, self.color, bar, 0)