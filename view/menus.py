import os, sys
sys.path.append(os.path.abspath('../'))
from controller import *
import pygame
from Common import *
pygame.font.init()
menuFont = pygame.font.SysFont("monospace",62)

class Menu(EventObject):
    event_system = Controller.event_system
    ###holds all the data for a single menu state instance
    def __init__(self,name,buttons,butCol=(255,255,255),txtCol=(255,255,0)):
        EventObject.__init__(self)
        self.name = name
        self.buttons = buttons
        self.butCol = butCol
        self.txtCol = txtCol
        self.title = Title(self.name)

    def draw(self,screen,offX=0,offY=0):
        if self.title:
            self.title.draw(screen,self.txtCol,[offX,offY])
        for but in self.buttons:
            but.draw(screen,self.txtCol,[offX,offY])


class Title(EventObject):
    event_system = Controller.event_system
    def __init__(self,text,x=-125,y=-400):
        EventObject.__init__(self)
        self.text = text
        self.location = [x,y]

    def draw(self,screen,txtColour,offset):
        label = menuFont.render(self.text,1,txtColour)
        screen.blit(label,(screen.get_width()/2 + self.location[0] + offset[0],screen.get_height()/2 + self.location[1] + offset[1]))

class Button(EventObject):
    event_system = Controller.event_system
    def __init__(self,text,x,y,colour=(255,255,255),rect=None):
        EventObject.__init__(self)
        self.text = text
        self.location = [x,y]
        self.colour = colour
        self.dimensions = menuFont.size(self.text)
    def draw(self,screen,txtColour,offset):
        label = menuFont.render(self.text,1,txtColour)
        self.rect = pygame.draw.rect(screen,self.colour,(screen.get_width()/2 + self.location[0] + offset[0],screen.get_height()/2 + self.location[1] + offset[1],self.dimensions[0],self.dimensions[1]))
        screen.blit(label,(screen.get_width()/2 + self.location[0] + offset[0],screen.get_height()/2 + self.location[1] + offset[1]))

menuList = {
    "pause" : Menu("Pause", (
        #       Name        X       Y
        Button("Resume",    -125,   -275),
        Button("Options",   -125,   -100),
        Button("Quit",      -125,   75)
        )),
    "options" : Menu("Options", (
        Button("Test",      -125, 0),
        Button("Back",      -125,   75)
        ))
    }
