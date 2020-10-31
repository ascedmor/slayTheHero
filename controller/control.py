import os, sys
sys.path.append(os.path.abspath('../'))
import pygame
from .EventSystem import *

class controller:
    event_system = EventSystem()
    event_system.add_event_type(QUIT_EVENT)
    event_system.add_event_type(KEYDOWN_EVENT)
    event_system.add_event_type(KEYUP_EVENT)
    event_system.add_event_type(BUTTON_CLICKED_EVENT)
    event_system.add_event_type(UPDATE_EVENT)
    event_system.add_event_type(UPDATE_FPS_EVENT)
    event_system.add_event_type(TOGGLE_FULLSCREEN_EVENT)
    event_system.add_event_type(UPDATE_MOUSE_EVENT)
    event_system.add_event_type(PAUSE_GAME_EVENT)
    event_system.add_event_type(LOAD_ROOM_EVENT)
    event_system.add_event_type(MAIN_LOOP_EVENT)
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.paused = True
        self.event_system.add_event_handler(PAUSE_GAME_EVENT, 0, self.pause)
        self.event_system.add_event_handler(MAIN_LOOP_EVENT, 0, self.main_loop)

    def on_close(self, event):
        self.running = False

    def pause(self, event):
        if event.event_object:
            self.paused = True
        else:
            self.paused = False

    def main_loop(self, event):
        if self.running:
            self.clock.tick(60)
            # Fire the 0th UPDATE_FPS_EVENT handler and pass in self.clock, this event should update the fps in the window
            self.event_system.FireEvent(self.clock, UPDATE_FPS_EVENT, 0)
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.event_system.FireEvent(None, QUIT_EVENT, 0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.event_system.FireEvent(None, TOGGLE_FULLSCREEN_EVENT, 0)
                    else:
                        select = True
                elif event.key == pygame.K_ESCAPE:
                    self.event_system.FireEvent(True, PAUSE_GAME_EVENT, 0)
                else:
                    if event.key == pygame.K_s or event.key == pygame.K_w:
                        self.event_system.FireEvent(event.key, KEYDOWN_EVENT, 1) #player move down
                    if event.key == pygame.K_d or event.key == pygame.K_a:
                        self.event_system.FireEvent(event.key, KEYDOWN_EVENT, 2) #player move right
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s or event.key == pygame.K_w:
                    self.event_system.FireEvent(event.key, KEYUP_EVENT, 1) #player move down
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    self.event_system.FireEvent(event.key, KEYUP_EVENT, 2) #player move right
                if event.key == pygame.K_RETURN:
                    select = False
        self.event_system.FireEvent(None, UPDATE_MOUSE_EVENT, 0)
        self.event_system.FireEvent(self.paused, UPDATE_EVENT, 0) # Update model
