import pygame

from . import scenes, events, objects

class PyCutGame():
    """docstring for PyCutGame"""
    def __init__(self):
        self.data = None
        #pre-inits for pygame?
        pygame.mixer.pre_init(44100, -16, 1, 512*2)
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.init(44100)
        ########################
        self.screen = pygame.display.get_surface()
        self.width = 1000
        self.height = 900
        self.fps = 15
        self.title = "PyCut"
        self.game_icon = pygame.image.load("game/assets/img/PyCut_icon.png")
        self.font_path  = "game/assets/font/Roboto-Thin.ttf"
        self.bold_font_path  = "game/assets/font/Roboto-Regular.ttf"
        self.shop_background = pygame.image.load("game/assets/img/Background.png")
        self.counter_top = pygame.image.load("game/assets/img/Countertop.png")
        self.help_img = pygame.image.load("game/assets/img/help.png")
        self.plain_pizza = pygame.image.load("game/assets/img/blank_pizza.png")
        self.button_bg = pygame.image.load("game/assets/img/red_button01.png")
        self.button_bg_active = pygame.image.load("game/assets/img/red_button02.png")
        self.message_bubble_img = pygame.image.load("game/assets/img/message_bubble.png")
        self.cheese_img = pygame.image.load("game/assets/img/cheese.png")
        self.mushroom_img = pygame.image.load("game/assets/img/mushroom.png")
        self.pepperoni_img = pygame.image.load("game/assets/img/pepperoni.png")
        self.pineapple_img = pygame.image.load("game/assets/img/pineapple.png")
        self.trash_can_img = pygame.image.load("game/assets/img/trash_can.png")
        self.trash_can_front_img = pygame.image.load("game/assets/img/trash_can_front.png")
        self.trash_can_back_img = pygame.image.load("game/assets/img/trash_can_back.png")
        self.character_1 = pygame.image.load("game/assets/img/Character1.png")
        self.character_2 = pygame.image.load("game/assets/img/Character2.png")
        self.character_3 = pygame.image.load("game/assets/img/Character3.png")
        self.character_4 = pygame.image.load("game/assets/img/Character4.png")
        self.game_characters = [self.character_1, self.character_2,
                                self.character_3, self.character_4]
        self.game_toppings = [self.cheese_img, self.mushroom_img,
                                self.pepperoni_img, self.pineapple_img]
        self.quit_attempt = False
        self.level = 1
        self.total_good_pizza = 0
        #everything necessary for the game should be initialized before here
        #the context is established based on these details and passed along to the active scene
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(self.font_path, 72)
        self.font = pygame.font.Font(self.font_path, 24)
        self.font_small = pygame.font.Font(self.font_path, 14)
        self.bold_font_large = pygame.font.Font(self.bold_font_path, 72)
        self.bold_font = pygame.font.Font(self.bold_font_path, 24)
        self.bold_font_small = pygame.font.Font(self.bold_font_path, 14)
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.game_icon)
        self.starting_scene = scenes.TitleScene
        self.active_scene = self.starting_scene(self)
        """    def write(self, text, center, size=self.size):
        = pygame.font.Font"""

    def game_loop(self):
        while self.active_scene != None:
            pressed_keys = pygame.key.get_pressed()
            # Event filtering
            filtered_events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_attempt = True
                elif event.type == pygame.KEYDOWN:
                    alt_pressed = pressed_keys[pygame.K_LALT] or \
                                  pressed_keys[pygame.K_RALT]
                    if event.key == pygame.K_ESCAPE:
                        self.quit_attempt = True
                    elif event.key == pygame.K_F4 and alt_pressed:
                        self.quit_attempt = True

                if self.quit_attempt:
                    self.active_scene.Terminate()
                else:
                    filtered_events.append(event)

            self.active_scene.ProcessInput(filtered_events, pressed_keys)
            self.active_scene.Update()
            self.active_scene.Render()

            self.active_scene = self.active_scene.next

            pygame.display.flip()
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()

    def quit(self):
        self.quit_attempt = True
