import pygame
from game.events import Clickable, Hoverable
from . import STATE, STATES, STYLES_NAMES as SM

class Button(Clickable, Hoverable):
    """docstring for Button"""
    def __init__(self, context, label=""):
        Clickable.__init__(self)
        Hoverable.__init__(self)
        self.context = context
        self.setState(STATE.NORMAL)
        self.label = label
        self.x = None
        self.y = None
        self.location = (0,0)
        self.width = None
        self.height = None
        self.style = dict()
        """
            Attributes that change due to state should be in the for loop below
        """
        for state in STATES:
            self.style[state] = dict()
            self.style[state][SM.BACKGROUND_IMG] = None
            self.style[state][SM.BACKGROUND_COLOR] = None
            #Any styling property with defaulst should be in
            #the conditional below
            if state == STATE.NORMAL:
                self.style[state][SM.COLOR] = (255, 255, 255)
                self.style[state][SM.PEN] = self.context.font
            else:
                self.style[state][SM.COLOR] = None
                self.style[state][SM.PEN] = None

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
        update the button drawing surface.
    """
    def draw(self):
        surf = None
        color = self.style[self.state][SM.COLOR]
        pen = self.style[self.state][SM.PEN]
        if not color:
            color = self.style[STATE.NORMAL][SM.COLOR]
        if not pen:
            pen = self.style[STATE.NORMAL][SM.PEN]
        if self.width and self.height:
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            #Various styles are handled bellow
            #if there is a styling for current state, use it otherwise use the
            #styling for the NORMAL state.
            if self.style[self.state][SM.BACKGROUND_COLOR]:
                surf.fill(self.style[self.state][SM.BACKGROUND_COLOR])
            elif self.style[STATE.NORMAL][SM.BACKGROUND_COLOR]:
                surf.fill(self.style[STATE.NORMAL][SM.BACKGROUND_COLOR])
            if self.style[self.state][SM.BACKGROUND_IMG]:
                surf.blit(pygame.transform.scale(self.style[self.state][SM.BACKGROUND_IMG], (self.width, self.height)), (0,0), [0, 0, self.width, self.height], special_flags = 0)
            elif self.style[STATE.NORMAL][SM.BACKGROUND_IMG]:
                surf.blit(self.style[STATE.NORMAL][SM.BACKGROUND_IMG], (0,0), [0, 0, self.width, self.height], special_flags = 0)
            text = pen.render(self.label, True, color)
            surf.blit(text, ((self.width - text.get_width()) // 2,
                         (self.height - text.get_height()) // 2 ))
        else:
            surf = pen.render(self.label, True, color)
        self.drawing = surf
        self.width = self.drawing.get_width()
        self.height = self.drawing.get_height()
        self.dirty = False;

    """
        draw on a surface
    """
    def drawOn(self, screen=None):
        if screen:
            if self.dirty:
                self.draw()
            screen.blit(self.drawing, self.location)
        else:
            print("Error: drawOn was called on Button object but no screen argument was passed")
        self.is_dirty = False

    """
    change the font size
    """
    def setPen(self, font, state=STATE.NORMAL):
        self.style[state][SM.PEN] = font
        self.draw()

    """
    change the font size
    """
    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.draw()

    """
    change the color
    """
    def setColor(self, color=(255, 255, 255), state=STATE.NORMAL):
        self.style[state][SM.COLOR] = color
        self.draw()

    """
    change the background color
    """
    def setBackgroundColor(self, bg_color=pygame.SRCALPHA, state=STATE.NORMAL):
        self.style[state][SM.BACKGROUND_COLOR] = bg_color
        self.draw()

    """
    change the background color
    """
    def setBackgroundImg(self, bg_img, state=STATE.NORMAL):
        self.style[state][SM.BACKGROUND_IMG] = bg_img
        if state == STATE.NORMAL:
            self.setSize(bg_img.get_width(), bg_img.get_height())

    """
    x,y are the center points of the button.
    """
    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.location = (x, y)
