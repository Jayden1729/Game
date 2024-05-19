import pygame
import pygame_gui

class GUI:

    def __init__(self, screen_width, screen_height):
        '''Initialises the GUI class.

        Args:
            screen_width (int): the width of the screen.
            screen_height (int): the height of the screen.
        '''
        button_rect = (screen_width / 4, screen_height / 10)
        screen_centre = (screen_width / 2 - button_rect[0] / 2, screen_height / 2 - button_rect[1] / 2)
        centre_offset = screen_height / 16

        self.paused = True

        self.manager = pygame_gui.UIManager((screen_width, screen_height))
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                                                    (screen_centre[0], screen_centre[1] - centre_offset), button_rect),
                                                    text='Start Game',
                                                    manager=self.manager)

        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                                                    (screen_centre[0], screen_centre[1] + centre_offset), button_rect),
                                                    text='Exit Game',
                                                    manager=self.manager)

        self.retry_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                                                    (screen_centre[0], screen_centre[1] - centre_offset), button_rect),
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
