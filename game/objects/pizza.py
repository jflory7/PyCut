import pygame
from pygame import gfxdraw
from .rangable import Rangable
from random import randint

class Pizza(Rangable):
    """docstring for Pizza"""
    def __init__(self, context):
        Rangable.__init__(self)
        self.context = context
        self.pizza = self.context.plain_pizza
        self.trashed = False
        self.perfected = False
        self.trashing = False
        self.trash_can = None
        self.trash_pos = None
        self.slices = None
        self.offset = randint(0,4)
        self.color=(0,0,0)
        self.x = 100
        self.y = 400 # 5=> margin between top and pizza
        self.location = (self.x,self.y)
        self.width = 150
        self.height = 150
        self.toppings = []
        self.requirements = []
        self.drawing = None
        self.draw()

    """
        update the button drawing surface.
    """
    def draw(self):
        S = 8 #speed towards trash can
        A = 9.8 #acceleration towards trash can
        if self.trashing:
            if self.touches(self.trash_can):
                self.trashed = True
                self.trashing = False
            else:
                self.setLocation(self.trash_pos[0] + 50, self.y + ((S)*A) )
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pizza_img = pygame.transform.scale(self.context.plain_pizza, (self.width, self.height))
        surf.blit(pizza_img, (0,0))
        for topping in self.toppings:
            self.drawTopping(surf, topping, 0)
        #gfxdraw.filled_ellipse(surf, self.width//2,self.height//2, self.width/2, self.height/2, (219,162,74))#pizza
        #pygame.draw.arc(surf, (225,216,0), [0, 0, self.width, self.height], 0, 360, 2)#crust
        #draw slices on here afterwards
        self.drawing = surf

    """
        draw on a surface
    """
    def drawOn(self, screen=None):
        if screen:
            self.draw()
            screen.blit(self.drawing, self.location)
        else:
            print("Error: drawOn was called on Button object but no screen argument was passed")

    """
        return topping drawing
    """
    def drawTopping(self, surf, topping_img, pad=0):
        #needs serious refactoring
        topping_img = pygame.transform.scale(topping_img, (self.width/4, self.height/4))
        degree = 0
        #center portion
        surf.blit(topping_img, ( (surf.get_width()/2) - (topping_img.get_width()/2), (surf.get_height()/2) - (topping_img.get_height()/2)))
        #top portion
        w,h = (surf.get_width()/6) + pad, surf.get_height()/6
        surf.blit( pygame.transform.rotate(topping_img, 45), ( w, h ))
        surf.blit( pygame.transform.rotate(topping_img, 45), ( 3*w , h ))
        #bottom portion
        surf.blit( pygame.transform.rotate(topping_img, 45), ( w, 3*h ))
        surf.blit( pygame.transform.rotate(topping_img, 45), ( 3*w , 3*h ))

        degree += 45
        return surf

    """
        draw on a surface
    """
    def moveToTrash(self, trash_pos=None, trash_can=None):
        if not(self.trashing or self.trashed):
            if trash_pos and trash_can:
                self.trash_pos = trash_pos
                self.trash_can = pygame.Rect((trash_pos[0], trash_pos[1]+self.height), (trash_can.get_width(), trash_can.get_height()))
                self.trashing = True
                self.setLocation(trash_pos[0] + 50, 200)
            else:
                print("Error: expected a trash_pos, trash_can got {}, {}".format(trash_pos, trash_can))

    """
        Add topping
    """
    def addTopping(self, topping):
        if not(self.trashing or self.trashed):
            if topping not in self.toppings:
                self.toppings += [topping]
            else:
                self.toppings.remove(topping)

    """
        set Costumer hidden Pizza requirements
    """
    def setRequirements(self, requirements):
        self.requirements = requirements

    """
        Checks if Pizza meets customer requirements.
        Currently only support topping requirements
        returns a tuple, boolean indicating whether it met the requirement
        or not. (Boolean, Message)
    """
    def checkRequirements(self):
        message = []
        metRequirement = False
        notwanted = 0
        missing = len(self.requirements) - len(self.toppings)
        for topping in self.toppings:
            if topping not in self.requirements:
                notwanted += 1
        if missing > 0:
            message += ["There is too little toppings on the pizza. :(".format(notwanted)]
        elif missing < 0:
            message += ["There is too much toppings on the pizza than I wanted. :(".format(notwanted)]
        if notwanted > 0:
            message += ["There is {} topping on the pizza I don't like. :(".format(notwanted)]
        if not(notwanted) and missing == 0:
            metRequirement = True
            message += ["Thank you! That was the perfect Pizza I was looking for :)\n"]
        return (metRequirement, message)

    """
        draw on a surface
    """
    def setPerfect(self):
        self.perfected = True

    """
    x,y are the center points of the text.
    """
    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.location = (x, y)
