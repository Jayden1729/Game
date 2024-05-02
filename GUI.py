import pygame
import pygame_gui

class GUI:

    def __init__(self):
        self.paused = True

        self.manager = pygame_gui.UIManager((800, 600))
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 315), (100, 50)),
                                                    text='Start Game',
                                                    manager=self.manager)

        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 385), (100, 50)),
                                                   text='Exit Game',
                                                   manager=self.manager)

    def show_main_menu(self):
        self.start_button.show()
        self.exit_button.show()

    def hide_main_menu(self):
        self.start_button.hide()
        self.exit_button.hide()
