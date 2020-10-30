import pygame
from .menus import *

class window:
    def __init__(self,width,height):
        self.running = True
        self.fullscreen = False
        self.room = None
        self.width = width
        self.height = height
        pygame.init()
        self.screen=pygame.display.set_mode([self.width,self.height])
        self.menu = None
        self.fps = 0

    def update(self,player,npcList,paused):
        if self.room != None:
            ###update background
            self.screen.blit(self.room.background,(player.cameraLocation[0]*-1,player.cameraLocation[1]*-1))
            ###update npc positions
            for this in self.room.npcs:
                screenLocation = (this.roomLocation[0] - player.cameraLocation[0],this.roomLocation[1] - player.cameraLocation[1])
                if screenLocation[0] >= 0 and screenLocation[0] <= self.width:
                    if screenLocation[1] >= 0 and screenLocation[1] <= self.height:
                        pygame.draw.circle(self.screen,(127,127,127),(screenLocation[0],screenLocation[1]),10)
            ###update player position
            pygame.draw.circle(self.screen,(255,255,255),(player.screenLocation[0],player.screenLocation[1]),10)
            if paused:
                if self.menu == None:
                    #Set pause as active menu
                    self.menu = menuList["pause"]
            else:
                self.menu = None
            if self.menu != None:
                self.menu.draw(self.screen)
        self.txt_at_location(self.fps,(50,50),menuFont)
        pygame.display.flip()

    def on_quit(self):
        self.running = False
        pygame.display.quit()

    def txt_at_location(self,text,screenLocation,font,colour=(0,0,0)):
        text = str(text)
        surface = font.render(text, 1, colour,(200,200,200))
        self.screen.blit(surface,screenLocation)

    def toggle_fullscreen(self):
        pygame.display.quit()
        if self.fullscreen == False:
            self.fullscreen = True
            self.screen = pygame.display.set_mode([self.width,self.height],pygame.FULLSCREEN)
        else:
            self.fullscreen = False
            self.screen = pygame.display.set_mode([self.width,self.height])

    def load_room(self,room):
        self.room = room
