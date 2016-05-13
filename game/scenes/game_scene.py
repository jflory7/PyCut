import random
import pygame
from . import SceneBase
from game.objects import STATE, Text, Button, Pizza, MessageBubble

class GameScene(SceneBase):
    def __init__(self, context):
        SceneBase.__init__(self, context)
        self.level = self.context.level
        self.game_over = False
        self.leveling_up = False
        self.buttons = []
        self.bad_pizzas = []
        self.good_pizzas = []
        self.game_toppings = self.context.game_toppings
        self.characters = self.context.game_characters
        self.current_pizza = None
        self.createGameMenu()
        self.createMessageBubble()
        self.buildPizzas()
        self.createToppingOptions()
        self.pizza_count_msg = Text(self.context, "{} Pizzas left".format(len(self.pizzas)))
        self.pizza_count_msg.setPen(self.context.font)
        self.pizza_count_msg.setColor((0, 0, 0))
        self.pizza_count_msg.setLocation(350, 675)
        self.game_over_msg =   Text(self.context, "Game Over!!!")
        self.game_over_msg.setPen(self.context.bold_font_large)
        self.game_over_msg.setColor((255,140,0))
        self.game_over_msg.setLocation((self.screen.get_width()/2) -(self.restart_button.width/2), 300)
        self.level_up_msg =   Text(self.context, "New Level reached")
        self.level_up_msg.setPen(self.context.bold_font_large)
        self.level_up_msg.setColor((255,140,0))
        self.level_up_msg.setLocation((self.screen.get_width()/2) -(self.restart_button.width/2), 300)
        self.continue_button = Button(self.context, "continue")
        self.continue_button.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.continue_button.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.continue_button.setOnLeftClick(self.handleContinueButtonClick)
        self.continue_button.setLocation( (self.screen.get_width()/2) -(self.continue_button.width/2) ,
            (self.screen.get_height()/2) - (self.continue_button.height/2) )
        self.createTrashCan()
        self.addCookingButton()
        self.generateCurrentPizzaRequirements()
        self.count = 0#for debugging

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.isClicked(event)
                if self.leveling_up:
                    self.continue_button.isClicked(event)

            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.isClicked(event)
                if self.leveling_up:
                    self.continue_button.isClicked(event)

            if event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.isHovered(event)
                if self.leveling_up:
                    self.continue_button.isHovered(event)

    def Update(self):
        self.count += 1
        self.checkForGoodPizzas()
        self.checkForTrashedPizzas()
        self.pizza_count_msg.setText("{} Pizzas left".format(len(self.pizzas)))
        self.levelDisplay.setText("Level: {}".format(self.level))
        #self.message_bubble.addMessage( "Pizza #: {}".format(self.count))

    def Render(self):
        # The game scene is just a blank blue screen
        self.screen.fill((244, 101, 36))
        self.screen.blit(self.context.shop_background,(0,0))
        self.screen.blit(self.characters[self.level% len(self.characters)],(850,255))
        self.screen.blit(self.context.counter_top,(0,0))
        self.message_bubble.drawOn(self.screen)
        if self.game_over:
            self.restart_button.setLocation( (self.screen.get_width()/2) -(self.restart_button.width/2) ,
                (self.screen.get_height()/2) - (self.restart_button.height/2) )
            self.restart_button.drawOn(self.screen)
            self.game_over_msg.drawOn(self.screen)
        elif self.leveling_up:
            self.level_up_msg.drawOn(self.screen)
            self.continue_button.drawOn(self.screen)
        else:
            for button in self.buttons:
                button.drawOn(self.screen)

        self.screen.blit(self.trashCanBack, (1000,600))
        #draw pizzas in the trash can
        for pizza in self.bad_pizzas:
            pizza.drawOn(self.screen)
        #then draw available pizzas
        for pizza in self.pizzas:
            pizza.drawOn(self.screen)
        self.pizza_count_msg.drawOn(self.screen)
        self.screen.blit(self.trashCanFront, (1000,600))

    """
        Take care of element initialization and event handlers bellow
    """

    def createGameMenu(self):
        P, K, Y = 300, 5, 30
        currX = P
        self.quit_button = Button(self.context, "Quit")
        self.quit_button.setPen(self.context.font)
        self.quit_button.setColor((255, 255, 255))
        self.quit_button.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.quit_button.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.quit_button.setOnLeftClick(self.handleQuitButtonClick)
        self.quit_button.setOnHover(self.handleQuitButtonHover)
        self.quit_button.setLocation(P, Y)
        currX+= self.quit_button.width
        self.restart_button = Button(self.context, "Restart")
        self.restart_button.setPen(self.context.font)
        self.restart_button.setColor((255, 255, 255))
        self.restart_button.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.restart_button.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.restart_button.setOnLeftClick(self.handleRestartButtonClick)
        self.restart_button.setLocation(currX + K, Y)
        currX += self.restart_button.width + K
        self.home_button = Button(self.context, "Menu/Home")
        self.home_button.setPen(self.context.font)
        self.home_button.setColor((255, 255, 255))
        self.home_button.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.home_button.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.home_button.setOnLeftClick(self.handleHomeButtonClick)
        self.home_button.setLocation(currX + K, Y)
        currX += self.home_button.width + K
        self.levelDisplay = Text(self.context, "Level: {}".format(self.level))
        self.levelDisplay.setPen(self.context.bold_font)
        self.levelDisplay.setLocation(currX + K, Y+5)
        self.levelDisplay.setColor((0, 0, 0))
        self.buttons += [self.quit_button, self.restart_button, self.home_button, self.levelDisplay]

    """
    helper methods below this point
    """
    def handleQuitButtonHover(self):
        pass

    def handleQuitButtonClick(self):
        self.context.quit()

    def handleRestartButtonClick(self):
        self.SwitchToScene(GameScene, self.context)

    def handleContinueButtonClick(self):
        self.SwitchToScene(GameScene, self.context)

    def handleHomeButtonClick(self):
        self.SwitchToScene(self.context.starting_scene, self.context)

    def buildPizzas(self):
        self.pizzas = []
        Y = 0
        for i in xrange(0,11-self.level):
            pizza = Pizza(self.context)
            pizza.setLocation(140, 620-Y)
            Y+=5
            self.pizzas += [pizza]
        if len(self.pizzas) > 0:
            self.current_pizza = self.pizzas[-1]

    """
    Checks for Pizzas in the current game instance and if a pizza is trashed as
    denounced by the pizza_instance.trashed propety it adds it to the bad_pizzas
    pile and removes it from the available pizzas.
    """
    def checkForTrashedPizzas(self):
        limit, i, trashed = len(self.pizzas), 0, False
        if self.current_pizza:
            previous_requirements = self.current_pizza.requirements
        while i < limit:
            pizza = self.pizzas[i]
            if pizza.trashed:
                self.bad_pizzas += [self.pizzas.pop(i)]
                trashed = True
                limit -= 1
            i+=1
        if trashed:
            if limit > 0:
                self.current_pizza = self.pizzas[-1]
                self.current_pizza.setRequirements(previous_requirements)
            else:
                self.current_pizza = None
        if not self.current_pizza and (len(self.pizzas) <= 0):
            self.gameOver()

    """
    Checks for Pizzas in the current game instance and if a pizza is to
    the client's satisfaction as denounced by the pizza_instance.perfected
    propety it adds it to the good_pizzas pile and removes it from the
    available pizzas.
    """
    def checkForGoodPizzas(self):
        limit, i, perfected = len(self.pizzas), 0, False
        while i < limit:
            pizza = self.pizzas[i]
            if pizza.perfected:
                self.good_pizzas += [self.pizzas.pop(i)]
                perfected = True
                limit -= 1
            i+=1
        if perfected:
            if limit > 0:
                self.current_pizza = self.pizzas[-1]
                self.generateCurrentPizzaRequirements()
            else:
                self.current_pizza = None

    def createToppingOptions(self):
        X = 600
        Y = 650
        K = 10
        self.cheeseBtn = Button(self.context, "Cheese")
        self.cheeseBtn.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.cheeseBtn.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.cheeseBtn.setOnLeftClick(self.addCheeseTopping)
        self.cheeseBtn.setLocation(X, Y)
        self.mushroomBtn = Button(self.context, "Mushroom")
        self.mushroomBtn.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.mushroomBtn.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.mushroomBtn.setOnLeftClick(self.addMushroomTopping)
        self.mushroomBtn.setLocation(X, Y + self.cheeseBtn.height + K)
        self.pepperoniBtn = Button(self.context, "Pepperoni")
        self.pepperoniBtn.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.pepperoniBtn.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.pepperoniBtn.setOnLeftClick(self.addPepperoniTopping)
        self.pepperoniBtn.setLocation(X + self.cheeseBtn.width + K, Y)
        self.pineappleBtn = Button(self.context, "Pineapple")
        self.pineappleBtn.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.pineappleBtn.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.pineappleBtn.setOnLeftClick(self.addPineappleTopping)
        self.pineappleBtn.setLocation(X + self.mushroomBtn.width + K, Y + self.pepperoniBtn.height + K)
        self.buttons += [self.cheeseBtn, self.mushroomBtn, self.pepperoniBtn, self.pineappleBtn]

    def addCheeseTopping(self):
        if self.current_pizza:
            self.current_pizza.addTopping(self.context.cheese_img)

    def addMushroomTopping(self):
        if self.current_pizza:
            self.current_pizza.addTopping(self.context.mushroom_img)

    def addPepperoniTopping(self):
        if self.current_pizza:
            self.current_pizza.addTopping(self.context.pepperoni_img)

    def addPineappleTopping(self):
        if self.current_pizza:
            self.current_pizza.addTopping(self.context.pineapple_img)

    def addCookingButton(self):
        self.cook = Button(self.context, "Cook")
        self.cook.setLocation(120, 770)
        self.cook.setBackgroundImg(self.context.button_bg, STATE.NORMAL)
        self.cook.setBackgroundImg(self.context.button_bg_active, STATE.ACTIVE)
        self.cook.setOnLeftClick(self.handleCooking)
        self.buttons += [self.cook]

    def handleCooking(self):
        if self.current_pizza:
            validity = self.current_pizza.checkRequirements()
            if validity[0]:
                self.current_pizza.setPerfect()
                self.levelUp()
            else:
                self.current_pizza.moveToTrash((1000,600), self.trashCan)
            if validity[1]:
                self.message_bubble.addMessage(None, validity[1])

    def createMessageBubble(self):
        self.message_bubble = MessageBubble(self.context)

    def createTrashCan(self):
        self.trashCan = self.context.trash_can_img #trashcan is imaginary only back and front are drawn.
        self.trashCanFront = self.context.trash_can_front_img
        self.trashCanBack = self.context.trash_can_back_img

    def generateCurrentPizzaRequirements(self):
        requires = []
        for i in xrange(0, self.level):
            random.getrandbits(1)
        for topping in self.game_toppings:
            if bool(random.getrandbits(1)):
                requires += [topping]
        if self.current_pizza:
            self.message_bubble.addMessage("I need a pizza")
            self.current_pizza.setRequirements(requires)

    def levelUp(self):
        self.leveling_up = True
        self.context.total_good_pizza += 1
        if self.context.level < len(self.context.game_characters):
            self.context.level += 1
            print("Leveling up")
        else:
            print("Max level reached")

    def gameOver(self):
        self.game_over = True
