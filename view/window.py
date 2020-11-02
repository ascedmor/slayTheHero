import os, sys
sys.path.append(os.path.abspath('../'))
from controller import *
import pygame
from .menus import *

class Window:
    event_system = Controller.event_system
    def __init__(self,width,height):
        self.running = True
        self.fullscreen = False
        self.room = None
        self.width = width
        self.height = height
        pygame.init()
        self.screen=pygame.display.set_mode([self.width,self.height])
        self.menu = None
        self.fps = 0.0
        self.mouse_screen_location = pygame.mouse.get_pos()
        self.mouse_left_button, self.mouse_right_button, self.mouse_middle_bbutton = pygame.mouse.get_pressed()
        self.event_system.add_event_handler(UPDATE_FPS_EVENT, 0, self.update_fps)
        self.event_system.add_event_handler(TOGGLE_FULLSCREEN_EVENT, 0, self.toggle_fullscreen)
        self.event_system.add_event_handler(UPDATE_MOUSE_EVENT, 0, self.update_mouse)
        self.event_system.add_event_handler(LOAD_ROOM_EVENT, 0, self.load_room)

    def update_fps(self, event):
        self.fps = event.event_object.get_fps()

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

    def update_mouse(self, event):
        self.mouse_screen_location = pygame.mouse.get_pos()
        self.mouse_left_button, self.mouse_right_button, self.mouse_middle_bbutton = pygame.mouse.get_pressed()
###If there is an active menu, check if a button is being clicked
##I wonder if there is a better way; something that lets you hold the button code in the button class
###Perhaps a button.click function that holds a reference to the menu that it should open?
        if self.menu != None:
            for button in self.menu.buttons:
                if button.rect != None:
                    if button.rect.collidepoint(self.mouse_screen_location):
                        if self.mouse_left_button:
                            menu = self.menu.name
                            if menu == "Pause":
                                if button.text == 'Resume':
                                    self.event_system.FireEvent(False, PAUSE_GAME_EVENT, 0)
                                if button.text == 'Options':
                                    self.menu = menuList["options"]
                                    print( 'No options menu implemented')
                                if button.text == 'Quit':
                                    self.event_system.FireEvent(None, QUIT_EVENT, 0)
                                elif menu == "Options":
                                    if button.text == "Back":
                                        self.menu = menuList["pause"]

    def on_close(self, event):
        self.running = False
        pygame.display.quit()

    def txt_at_location(self,text,screenLocation,font,colour=(0,0,0)):
        text = str(text)
        surface = font.render(text, 1, colour,(200,200,200))
        self.screen.blit(surface,screenLocation)

    def toggle_fullscreen(self, event):
        pygame.display.quit()
        if self.fullscreen == False:
            self.fullscreen = True
            self.screen = pygame.display.set_mode([self.width,self.height],pygame.FULLSCREEN)
        else:
            self.fullscreen = False
            self.screen = pygame.display.set_mode([self.width,self.height])

    def load_room(self,event):
        self.room = event.event_object
