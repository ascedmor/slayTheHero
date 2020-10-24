import view
import model
import pygame
import menus

class controller:
    def __init__(self):
        width = 1440
        height = 960
        self.window = view.window(width,height)
        self.model = model.model(self.window)
        self.running = True
        self.clock = pygame.time.Clock()
        self.paused = True
        self.main_loop()
        
    def main_loop(self):
        moveUp = False
        moveDown = False
        moveLeft = False
        moveRight = False
        while self.running != False:
            self.clock.tick(60)
            self.window.fps = self.clock.get_fps()
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.window.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pygame.K_w:
                    moveUp = True
                if event.key == pygame.K_a:
                    moveLeft = True
                if event.key == pygame.K_s:
                    moveDown = True
                if event.key == pygame.K_d:
                    moveRight = True
                if event.key == pygame.K_RETURN:
                    select = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    moveUp = False
                if event.key == pygame.K_a:
                    moveLeft = False
                if event.key == pygame.K_s:
                    moveDown = False
                if event.key == pygame.K_d:
                    moveRight = False
                if event.key == pygame.K_RETURN:
                    select = False
            if not self.paused:
                if moveUp == True:
                    self.model.player.add_speed([0,-1])
                if moveDown == True:
                    self.model.player.add_speed([0,1])
                if moveRight == True:
                    self.model.player.add_speed([1,0])
                if moveLeft == True:
                    self.model.player.add_speed([-1,0])
                for this in self.model.rooms[self.model.activeRoom].npcs:
                    this.goto_location(self.model.player.playerLocation)
            else:
                mouseScreenLocation = pygame.mouse.get_pos()
                leftButton,rightButton,middleButton = pygame.mouse.get_pressed()
###If there is an active menu, check if a button is being clicked
##I wonder if there is a better way; something that lets you hold the button code in the button class
###Perhaps a button.click function that holds a reference to the menu that it should open?
                if self.window.menu != None:
                    for button in self.window.menu.buttons:
                        if button.rect != None:
                            if button.rect.collidepoint(mouseScreenLocation):
                                if leftButton:
                                    menu = self.window.menu.name
                                    print menu
                                    if menu == "Pause":
                                        if button.text == 'Resume':
                                            self.paused = False
                                        if button.text == 'Options':
                                            self.window.menu = menus.menuList["options"]
                                            print( 'No options menu implemented')
                                        if button.text == 'Quit':
                                            self.running = False
                                    elif menu == "Options":
                                        if button.text == "Back":
                                            self.window.menu = menus.menuList["pause"]
            self.model.update(self.paused)
        self.window.on_quit()
                
if __name__ == '__main__':
    c = controller()
