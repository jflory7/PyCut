from gettext import gettext as _

import sys

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import pygame

from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton


import sugargame.canvas
import game

class PyCutActivity(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.max_participants = 1

        # Create the game instance.
        self.game = game.PyCutGame(poll_cb=self._poll_cb)

        # Build the activity toolbar.
        self.build_toolbar()

        # Build the Pygame canvas.
        # Start the game running (self.game.run is called when the
        # activity constructor returns).
        self.game.canvas = sugargame.canvas.PygameCanvas(self,
            main=self.game.run, modules=[pygame.display, pygame.font])

        # Note that set_canvas implicitly calls read_file when
        # resuming from the Journal.
        self.set_canvas(self.game.canvas)
        self.game.canvas.grab_focus()

    def _poll_cb(self):
        while Gtk.events_pending():
            Gtk.main_iteration()
        if self.game.quit_attempt:
            Gtk.main_quit()

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        # Blank space (separator) and Stop button at the end:

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        stop_button.connect('clicked', self._stop_cb)

    def _stop_cb(self, button):
        self.game.running = False

    def read_file(self, file_path):
        self.game.read_file(file_path)

    def write_file(self, file_path):
        self.game.write_file(file_path)

    def get_preview(self):
        return self.game.canvas.get_preview()
