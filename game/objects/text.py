import pygame
from game.events import Clickable, Hoverable
from . import STATE, STATES, STYLES_NAMES as SM

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
        """
            Attributes that change due to state should be in the for loop below

            Notes:
                Only normal state has defaults, all others have None
        """
        for state in STATES:
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
        self.drawing = None
        self.draw()

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

    """
        draw on a surface
    """
    def drawOn(self, screen=None):
        if screen:
            self.draw()
            screen.blit(self.drawing, self.location)
        else:
            print("Error: drawOn was called on Text object but no screen argument was passed")

    """
        change the Text
    """
    def setText(self, text):
        self.text = text
        self.draw()

    """
    change the font size
    """
    def setPen(self, font, state=STATE.NORMAL):
        self.style[state][SM.PEN] = font
        self.draw()

    """
    change the color
    """
    def setColor(self, color=(0, 128, 0), state=STATE.NORMAL):
        self.style[state][SM.COLOR] = color
        self.draw()

    """
    x,y are the center points of the text.
    """
    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.location = (x, y)
