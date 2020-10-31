import os, sys
sys.path.append(os.path.abspath('../'))
from controller import *
import pygame
pygame.font.init()
menuFont = pygame.font.SysFont("monospace",62)

class menu:
    event_system = controller.event_system
    ###holds all the data for a single menu state instance
    def __init__(self,name,buttons,butCol=(255,255,255),txtCol=(255,255,0)):
        self.name = name
        self.buttons = buttons
        self.butCol = butCol
        self.txtCol = txtCol
        self.title = title(self.name)

    def draw(self,screen,offX=0,offY=0):
        if self.title:
            self.title.draw(screen,self.txtCol,[offX,offY])
        for but in self.buttons:
            but.draw(screen,self.txtCol,[offX,offY])


class title:
    event_system = controller.event_system
    def __init__(self,text,x=-125,y=-400):
        self.text = text
        self.location = [x,y]

    def draw(self,screen,txtColour,offset):
        label = menuFont.render(self.text,1,txtColour)
        screen.blit(label,(screen.get_width()/2 + self.location[0] + offset[0],screen.get_height()/2 + self.location[1] + offset[1]))

class button:
    event_system = controller.event_system
    def __init__(self,text,x,y,colour=(255,255,255),rect=None):
        self.text = text
        self.location = [x,y]
        self.colour = colour
        self.dimensions = menuFont.size(self.text)
    def draw(self,screen,txtColour,offset):
        label = menuFont.render(self.text,1,txtColour)
        self.rect = pygame.draw.rect(screen,self.colour,(screen.get_width()/2 + self.location[0] + offset[0],screen.get_height()/2 + self.location[1] + offset[1],self.dimensions[0],self.dimensions[1]))
        screen.blit(label,(screen.get_width()/2 + self.location[0] + offset[0],screen.get_height()/2 + self.location[1] + offset[1]))

menuList = {
    "pause" : menu("Pause", (
        #       Name        X       Y
        button("Resume",    -125,   -275),
        button("Options",   -125,   -100),
        button("Quit",      -125,   75)
        )),
    "options" : menu("Options", (
        button("Test",      -125, 0),
        button("Back",      -125,   75)
        ))
    }
