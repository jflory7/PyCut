import pygame
from game.events import Clickable, Hoverable
from . import STATE, STYLES_NAMES as SM

class Text(Hoverable, Clickable):
    """docstring for Text"""
    def __init__(self, context, text):
        Clickable.__init__(self)
        Hoverable.__init__(self)
        self.context = context
        self.state = STATE.NORMAL
        self.text = text
        self.x = None
        self.y = None
        self.location = (0,0)
        self.width = None
        self.height = None
        self.style = dict()
        self.centered = False
        
        self.checkState(STATE.NORMAL)
        self.checkState(STATE.ACTIVE)
        self.checkState(STATE.HOVER)
        self.checkState(STATE.INACTIVE)
        
        self.drawing = None
        self.draw()
        
    """
        initialize a state.
    """
    def checkState(self, state):
        self.style[state] = dict()
        self.style[state][SM.BACKGROUND_IMG] = None
        self.style[state][SM.BACKGROUND_COLOR] = None
        #Any styling property with defaulst should be in
        #the conditional below
        if state == STATE.NORMAL:
            self.style[state][SM.COLOR] = (0, 128, 0)
            self.style[state][SM.PEN] = self.context.font
        else:
            self.style[state][SM.COLOR] = None
            self.style[state][SM.PEN] = None

    """
        update the text drawing surface.
    """
    def draw(self):
        color = self.style[self.state][SM.COLOR]
        pen = self.style[self.state][SM.PEN]
        if not color:
            color = self.style[STATE.NORMAL][SM.COLOR]
        if not pen:
            pen = self.style[STATE.NORMAL][SM.PEN]
        self.drawing = pen.render(self.text, True, color)
        self.width = self.drawing.get_width()
        self.height = self.drawing.get_height()
        self.dirty = False

    """
        draw on a surface
    """
    def drawOn(self, screen=None):
        if screen:
            if self.dirty:
                self.draw()
            if self.centered:
                loc = (self.location[0] - self.width / 2, self.location[1])
                screen.blit(self.drawing, loc)
            else:
                screen.blit(self.drawing, self.location)
        else:
            print("Error: drawOn was called on Text object but no screen argument was passed")

    """
        change the Text
    """
    def setText(self, text):
        self.text = text
        self.dirty = True

    """
    change the font size
    """
    def setPen(self, font, state=STATE.NORMAL):
        self.style[state][SM.PEN] = font
        self.dirty = True

    """
    change the color
    """
    def setColor(self, color=(0, 128, 0), state=STATE.NORMAL):
        self.style[state][SM.COLOR] = color
        self.dirty = True

    """
    x,y are the center points of the text.
    """
    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.location = (x, y)
