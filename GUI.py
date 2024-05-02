import pygame
import pygame_gui

class GUI:

    def __init__(self):
        self.paused = True

        self.main_menu_manager = pygame_gui.UIManager((800, 600))
        self.main_menu = main_menu_design(self.main_menu_manager)

    def process_events(self, event):
        self.main_menu_manager.process_events(event)

    def show_main_menu(self):
        start_button.show()
        exit_button.show()

    def hide_main_menu(self):
        start_button.hide()
        exit_button.hide()

    def button_logic(self, event):

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                self.paused = False
                self.hide_main_menu()
                print('start')

def main_menu_design(manager):
    global start_button
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 315), (100, 50)),
                                                text='Start Game',
                                                manager=manager)

    global exit_button
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 385), (100, 50)),
                                                text='Exit Game',
                                                manager=manager)


