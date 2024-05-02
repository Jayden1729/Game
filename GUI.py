import pygame
import pygame_gui

class GUI:

    def __init__(self):
        self.paused = True

        self.manager = pygame_gui.UIManager((800, 600))
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 300), (200, 80)),
                                                    text='Start Game',
                                                    manager=self.manager)

        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 400), (200, 80)),
                                                   text='Exit Game',
                                                   manager=self.manager)

        self.retry_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 300), (200, 80)),
                                                    text='Retry',
                                                    manager=self.manager)
        self.retry_button.hide()

    def show_main_menu(self):
        self.start_button.show()
        self.exit_button.show()

    def hide_main_menu(self):
        self.start_button.hide()
        self.exit_button.hide()

    def show_retry_menu(self):
        self.retry_button.show()
        self.exit_button.show()

    def hide_retry_menu(self):
        self.retry_button.hide()
        self.exit_button.hide()
