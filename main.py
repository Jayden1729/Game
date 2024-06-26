# -*- coding: utf-8 -*-
"""
Naming conventions:

class: CapWords
variable: lower_case
constants: CAPITAL_CASE



"""

import csv
import copy

import pygame
import pygame_gui

import Images
import Level
import Player
import GUI



def main():
    # initialise pygame
    pygame.init()

    # Variables
    screen_width = 1024
    screen_height = 900
    screen_dimensions = [screen_width, screen_height]
    min_dimension = min(screen_width, screen_height)
    square_size = min_dimension / 16
    fps = 90
    show_hitboxes = True

    fps_total = 0
    frame_counter = 0

    # Setup initial objects
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    images = Images.Images(min_dimension)
    player = Player.Player(images.player_dict, screen_dimensions)
    gui = GUI.GUI(screen_width, screen_height)

    levels = []

    # Import levels
    for i in range(5):
        with open('Level_' + str(i + 1) + '.csv') as csvfile:
            reader = csv.reader(csvfile)
            game_grid = list(reader)
            for i in range(len(game_grid)):
                for j in range(len(game_grid[0])):
                    if game_grid[i][j] == '1':
                        game_grid[i][j] = 1
            levels.append(Level.Level(game_grid, square_size, images, screen_dimensions))

    level = copy.deepcopy(levels[0])
    current_level = 1

    running = True

    # Game Loop
    while running:
        current_fps = clock.get_fps()
        fps_total += current_fps
        frame_counter += 1

        # Fill screen background
        screen.fill((0, 0, 0))
        screen.blit(images.background, (0, 0))
        screen.blit(images.planet, (screen_width / 2 - 150, screen_height / 2 - 150))

        # Change Level if all enemies killed
        if not level.enemy_list:
            current_level += 1
            level = copy.deepcopy(levels[current_level - 1])

        # Get all pressed keys
        pressed_keys = pygame.key.get_pressed()

        # for loop through event queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if gui.paused:
                        gui.paused = False
                        gui.hide_main_menu()
                    elif not gui.paused:
                        gui.paused = True
                        gui.show_main_menu()

            if event.type == pygame.QUIT:
                running = False
            # Check if player is attacking
            elif (event.type == pygame.MOUSEBUTTONDOWN or pressed_keys[pygame.K_SPACE]) and player.attack_cooldown == 0:
                player.attack(level.player_bullets, screen_width, screen_height, images.bullet_dict)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gui.start_button:
                    gui.paused = False
                    gui.hide_main_menu()

                if event.ui_element == gui.exit_button:
                    running = False

                if event.ui_element == gui.retry_button:
                    gui.paused = False
                    gui.hide_retry_menu()
                    level = copy.deepcopy(levels[0])
                    current_level = 1

            # GUI
            gui.manager.process_events(event)

        if not gui.paused:
            images.display_wall_images(level, screen, screen_width, screen_height)
            images.display_floor_images(level, screen, screen_width, screen_height)

            # Determine enemy movement and draw them on screen
            for enemy in level.enemy_list:
                enemy.update_movement(level, player, 11)

                if show_hitboxes:
                    screen.blit(enemy.surf, enemy.rect)

                enemy.animate(screen)

                enemy.attack(level)

            # Show melee attack hitbox
            for attack in level.enemy_melee:
                if show_hitboxes:
                    screen.blit(attack.surf, attack.rect)
                if pygame.Rect.colliderect(attack.rect, player.rect):
                    level.time -= attack.damage
                attack.display_time -= 1
                if attack.display_time <= 0:
                    attack.kill()

            # Draw and move player bullets + check collisions
            level.update_player_bullets(screen, show_hitboxes)

            # Draw and move enemy bullets + check collisions
            level.update_enemy_bullets(screen, player, show_hitboxes)

            # Player movement and draw player
            player.move(level, pressed_keys)
            if show_hitboxes:
                screen.blit(player.surf, player.rect)
            player.animate(screen)

            # Reduce player attack cooldown
            if player.attack_cooldown > 0:
                player.attack_cooldown -= 1

            # Draw timer

            if level.time > 15000:
                level.time = 1500

            if level.time >= 10:
                time_surf = pygame.Surface(((level.time / 3), 20))
                timer = time_surf.get_rect(center=(screen_width/2, screen_height/20))
                pygame.draw.rect(screen, (0, 0, 100), timer)
            else:
                gui.paused = True
                gui.show_retry_menu()

            level.time -= 1

        # Update GUI
        gui.manager.update(fps)
        gui.manager.draw_ui(screen)

        pygame.display.flip()
        clock.tick(fps)
        #print(current_fps)

    pygame.quit()

    print('average fps = ' + str(fps_total/frame_counter))

if __name__ == '__main__':
    main()
