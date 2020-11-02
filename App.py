import os, sys
from Common import *
from controller import *
from view import *
from model import *

class App(EventObject):
    event_system = Controller.event_system
    def __init__(self):
        EventObject.__init__(self)
        self.event_system.add_event_handler(QUIT_EVENT, 0, self.on_close)
        self.controller = Controller()
        width = 1440
        height = 960
        self.window = Window(width,height)
        self.model = Model(self.window)
        self.main_loop()

    def on_close(self, event):
        self.event_system.on_close()
        self.controller.on_close(event)
        self.model.on_close(event)

    def main_loop(self):
        self.event_system.running = True
        while self.event_system.running:
            if self.controller.running:
                self.event_system.FireEvent(None, MAIN_LOOP_EVENT, 0)
            while len(self.event_system.event_queue)>0:
                self.event_system.process()
