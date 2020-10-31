import os, sys
sys.path.append(os.path.abspath('../'))
from controller import *
import pygame
import random
import numpy
import math
from PIL import Image as image
class model():
    event_system = controller.event_system
    def __init__(self,window):
        self.window = window
        self.player = player([500,500],self.window.width,self.window.height)
        ##create test room and set it as the active room
        self.rooms = {
            "Test": room(name="Test")
            }
        self.activeRoom = "Test"
        self.event_system.add_event_handler(UPDATE_EVENT, 0, self.update)
        count = 0
        ###Add 10 random npcs to the test map
        print('adding random npcs')
        while count < 10:
            self.rooms["Test"].add_npc(npc((random.randint(0,self.rooms[self.activeRoom].size[0]),random.randint(0,self.rooms[self.activeRoom].size[1])),random.randint(1,8)))
            count +=1
        print('finished adding npcs')
        self.event_system.FireEvent(self.get_room(), LOAD_ROOM_EVENT, 0)

    def add_room(self,room):
        self.rooms[room.name] = room

    def get_room(self):
        return self.rooms[self.activeRoom]

    def update(self, event):
        if not event.event_object:
            self.player.update_speed()
            for this in self.rooms[self.activeRoom].npcs:
                this.goto_location(self.player.playerLocation)
            self.player.update_location(self.window,self.rooms[self.activeRoom])
            for this in self.rooms[self.activeRoom].npcs:
                this.update_location(self.rooms[self.activeRoom])
        self.player.centre_camera(self.player.playerLocation,self.window,self.rooms[self.activeRoom],True)
        self.window.update(self.player,self.rooms[self.activeRoom].npcs,event.event_object)

    def on_close(self, event):
        self.window.on_close(event)

class room():
    event_system = controller.event_system
    def __init__(self, name, background=pygame.image.load('villageMap.bmp'), collision=pygame.image.load('testCollision.bmp')):
        self.background = pygame.transform.scale(background,(12000,12000))
        collision = pygame.transform.scale(collision,(12000,12000))
        self.size = self.background.get_rect().size
        collision = pygame.surfarray.array2d(collision)
        self.collision = collision
        self.npcs = []
        self.name = name

    def add_npc(self, npc):
        self.npcs.append(npc)

    #def save(self):
        ###This function will be used to save the room state when the player exits the room


class player():
    event_system = controller.event_system
    def __init__(self, location,windowWidth,windowHeight):
        ###do player stuff here
        self.playerLocation = location
        self.screenLocation = [windowWidth/2,windowHeight/2]
        self.cameraLocation = [location[0]-windowWidth/2,location[1]-windowHeight/2]
        self.velocity = [0.00,0.00]
        self.maxSpeed=10
        self.movement_modifier = 1.0
        self.move_down = 0.0
        self.move_right = 0.0
        self.event_system.add_event_handler(KEYDOWN_EVENT, 1, self.keydown_move_down)
        self.event_system.add_event_handler(KEYDOWN_EVENT, 2, self.keydown_move_right)
        self.event_system.add_event_handler(KEYUP_EVENT, 1, self.keyup_move_down)
        self.event_system.add_event_handler(KEYUP_EVENT, 2, self.keyup_move_right)

    def keydown_move_down(self, event):
        if event.event_object == pygame.K_s:
            self.move_down += self.movement_modifier
        else:
            self.move_down -= self.movement_modifier

    def keydown_move_right(self, event):
        if event.event_object == pygame.K_d:
            self.move_right += self.movement_modifier
        else:
            self.move_right -= self.movement_modifier

    def keyup_move_down(self, event):
        if event.event_object == pygame.K_s:
            self.move_down -= self.movement_modifier
        else:
            self.move_down += self.movement_modifier

    def keyup_move_right(self, event):
        if event.event_object == pygame.K_d:
            self.move_right -= self.movement_modifier
        else:
            self.move_right += self.movement_modifier

    def update_speed(self):
        self.add_speed([self.move_right,self.move_down])

    def add_speed(self,dd_vector):
        self.velocity = [self.velocity[0] + dd_vector[0],self.velocity[1] + dd_vector[1]]
        self.velocity[0] = clamp(self.velocity[0], -self.maxSpeed, self.maxSpeed)
        self.velocity[1] = clamp(self.velocity[1], -self.maxSpeed, self.maxSpeed)
        return self.velocity

    def update_location(self,window,room):
        ###move player
        cameraLocation = self.cameraLocation    #location of camera in room
        screenLocation = self.screenLocation    #location of player on camera
        playerLocation = self.playerLocation    #location of player in room
        playerLocation = [playerLocation[0] + math.trunc(self.velocity[0]), playerLocation[1] + math.trunc(self.velocity[1])]
        playerLocation[0] = clamp(playerLocation[0], 0, room.size[0])
        playerLocation[1] = clamp(playerLocation[1], 0, room.size[1])
        if room.collision[int(playerLocation[0]),int(playerLocation[1])] > 1:
            ###move player
            self.playerLocation = [int(playerLocation[0]),int(playerLocation[1])]
        else:
            return room.collision[int(playerLocation[0]),int(playerLocation[1])]
        self.velocity=[self.velocity[0]*0.9,self.velocity[1]*0.9]

    def centre_camera(self,centre,window,room,mouse=False):
        mouseScreenLocation = pygame.mouse.get_pos()
        cameraStickiness = 3
        offset = [self.screenLocation[0] - mouseScreenLocation[0],self.screenLocation[1] - mouseScreenLocation[1]]
        offset = [offset[0]/cameraStickiness,offset[1]/cameraStickiness]
        if not mouse:
            offset = [0,0]
##        if offset[0] > window.width/4:
##            offset[0] = window.width/4
##        elif offset[0] < - window.width/4:
##            offset[0] = - window.width/4
##        if offset[1] > window.height/4:
##            offset[1] = window.height/4
##        elif offset[1] < -window.height/4:
##            offset[1] = -window.height/4
        centre = [centre[0] - offset[0], centre[1] - offset[1]]
        centre = [centre[0] - window.width/2,centre[1] - window.height/2]
        centre[0] = clamp(centre[0], 0, room.size[0]-window.width)
        centre[1] = clamp(centre[1], 0, room.size[1]-window.height)
        self.cameraLocation = centre
        self.screenLocation = [self.playerLocation[0] - self.cameraLocation[0], self.playerLocation[1] - self.cameraLocation[1]]




class npc():
    event_system = controller.event_system
    def __init__(self, location,level):
        ###do entity init stuff here
        self.roomLocation = location
        ###type will hold a numerical value that indicates the type of npc (0=villager,1=monster tier 1,2=monster tier 2,3=monster tier 3,4=monster tier 4,5=monster tier 5,6=monster tier 6,7=world boss)
        self.type = level
        print(self.type)
        self.maxSpeed = float(self.type)
        self.velocity = [0.00,0.00]

    def goto_location(self,location):
        ###something weird happens in here with lower speed values

        vector = [location[0]-self.roomLocation[0],location[1]-self.roomLocation[1]]
        ###Speed impulse is relative to distance (if < 100) for smooth deceleration
        vector = [vector[0]*float(self.maxSpeed/100.0),vector[1]*float(self.maxSpeed/100.0)]
        if abs(vector[0]) > abs(vector[1]):
            try:
                vector = [clamp(vector[0],-1,1)*self.maxSpeed,vector[1]*(self.maxSpeed/abs(vector[0]))]
            except:
                pass
        else:
            try:
                vector = [vector[0]*(self.maxSpeed/abs(vector[1])),clamp(vector[1],-1,1)*self.maxSpeed]
            except:
                pass
        self.add_speed(vector,True)

    def add_speed(self,dd_vector,override=False):
        if not override:
            self.velocity = [self.velocity[0] + dd_vector[0],self.velocity[1] + dd_vector[1]]
        else:
            self.velocity = dd_vector
        self.velocity[0] = clamp(self.velocity[0], -self.maxSpeed, self.maxSpeed)
        self.velocity[1] = clamp(self.velocity[1], -self.maxSpeed, self.maxSpeed)
        return self.velocity

    def update_location(self,room):
        roomLocation = [math.trunc(self.roomLocation[0] + self.velocity[0]),math.trunc(self.roomLocation[1] + self.velocity[1])]
        roomLocation[0] = clamp(roomLocation[0], 0, room.size[0]-1)
        roomLocation[1] = clamp(roomLocation[1], 0, room.size[1]-1)
        if room.collision[int(roomLocation[0]),int(roomLocation[1])] > 1:
            ###move npc
            self.roomLocation = [int(roomLocation[0]),int(roomLocation[1])]
        self.velocity=[self.velocity[0]*0.9,self.velocity[1]*0.9]



        class ability():
            def __init__(self,name=None):
                ###ability sub class
                self.name = name


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
