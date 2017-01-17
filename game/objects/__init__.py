class STATE:
    """docstring for STATE"""
    NORMAL = 0;
    ACTIVE = 1;
    HOVER = 2;
    INACTIVE = 3;

STATES = [STATE.NORMAL, STATE.ACTIVE, STATE.HOVER, STATE.INACTIVE]

class STYLES_NAMES:
    """docstring for STYLES"""
    COLOR = "color";
    BACKGROUND_IMG = "background_img";
    BACKGROUND_COLOR = "background_color";
    PEN = "pen";

from .button import Button
from .text import Text
from .slice import Slice
from .pizza import Pizza
from .message_bubble import MessageBubble
from .toggle import Toggle
