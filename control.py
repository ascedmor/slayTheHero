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
        moveDown = 0.0
        moveRight = 0.0
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
                    moveDown -= 1.0
                elif event.key == pygame.K_s:
                    moveDown += 1.0
                if event.key == pygame.K_a:
                    moveRight -= 1.0
                elif event.key == pygame.K_d:
                    moveRight += 1.0
                if event.key == pygame.K_RETURN:
                    select = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    moveDown += 1.0
                elif event.key == pygame.K_s:
                    moveDown -= 1.0
                if event.key == pygame.K_a:
                    moveRight += 1.0
                elif event.key == pygame.K_d:
                    moveRight -= 1.0
                if event.key == pygame.K_RETURN:
                    select = False
            if not self.paused:
                self.model.player.add_speed([moveRight,moveDown])
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
                                    print(menu)
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
