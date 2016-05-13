import pygame
from . import SceneBase
from game.objects import Text, Button, STATE

class HelpScene(SceneBase):
    def __init__(self, context):
        SceneBase.__init__(self, context)
        self.buttons = []
        self.createGameMenu()

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.isClicked(event)

            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.isClicked(event)

            if event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.isHovered(event)

    def Update(self):
        pass

    def Render(self):
        # For the sake of brevity, the title scene is a blank red screen
        self.screen.fill((244, 101, 36))
        self.screen.blit(self.context.help_img,
                ( (self.context.width - self.context.help_img.get_width()) // 2,
                 ((self.context.height - self.context.help_img.get_height())  // 2)))
        for button in self.buttons:
            button.drawOn(self.screen)
        #self.screen.blit(self.start_button.draw(),
        #        ( (self.context.width - self.start_button.width) // 2,
        #         ((self.context.height - self.start_button.height) + self.title.get_height()) // 2))
        #pygame.draw.rect(self.screen, (0, 100, 100), pygame.Rect(100, 100, 200, 200))


    def createGameMenu(self):
        P, K, Y = 300, 5, 30
        currX = P
        self.quit_button = Button(self.context, "Quit")
        self.quit_button.setPen(self.context.font)
        self.quit_button.setColor((255, 255, 255))
        self.quit_button.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.quit_button.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.quit_button.setOnLeftClick(self.handleQuitButtonClick)
        self.quit_button.setLocation(P, Y)
        currX+= self.quit_button.width
        self.home_button = Button(self.context, "Menu/Home")
        self.home_button.setPen(self.context.font)
        self.home_button.setColor((255, 255, 255))
        self.home_button.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.home_button.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.home_button.setOnLeftClick(self.handleHomeButtonClick)
        self.home_button.setLocation(currX + K, Y)
        self.buttons += [self.quit_button, self.home_button]
    """
    helper methods below this point
    """
    def handleQuitButtonClick(self):
        self.context.quit()

    def handleHomeButtonClick(self):
        self.SwitchToScene(self.context.starting_scene, self.context)
