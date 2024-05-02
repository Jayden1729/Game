# -*- coding: utf-8 -*-
"""
Naming conventions:

class: CapWords
variable: lower_case
constants: CAPITAL_CASE



"""

import csv

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
    screen_width = 800
    screen_height = 800
    square_size = 50
    fps = 90
    show_hitboxes = False

    # Setup initial objects
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    player = Player.Player()
    images = Images.Images(square_size)
    gui = GUI.GUI()

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
            levels.append(Level.Level(game_grid, square_size))

    level = levels[0]
    current_level = 1

    running = True

    # Game Loop
    while running:

        # Fill screen background
        screen.fill((0, 0, 0))

        # Change Level if all enemies killed
        if not level.enemy_list:
            current_level += 1
            level = levels[current_level - 1]

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
            elif event.type == pygame.QUIT:
                running = False
            # Check if player is attacking
            elif (event.type == pygame.MOUSEBUTTONDOWN or pressed_keys[pygame.K_SPACE]) and player.attack_cooldown == 0:
                player.attack(level.player_bullets)

            gui.button_logic(event)

            # GUI
            gui.process_events(event)

        if not gui.paused:
            images.display_wall_images(level, screen)
            images.display_floor_images(level, screen)

            # Determine enemy movement and draw them on screen
            for enemy in level.enemy_list:
                enemy.update_movement(level, player, 12, 16)

                if show_hitboxes:
                    screen.blit(enemy.surf, enemy.rect)

                enemy.animate(images, screen)

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
            level.update_player_bullets(screen)

            # Draw and move enemy bullets + check collisions
            level.update_enemy_bullets(screen, player)

            # Player movement and draw player
            move_player(level, player, pressed_keys)
            screen.blit(player.surf, player.rect)
            screen.blit(player.sprite, (367, 358))

            # Reduce player attack cooldown
            if player.attack_cooldown > 0:
                player.attack_cooldown -= 1

            # Draw timer
            if level.time <= 0:
                running = False

            if level.time > 1000:
                level.time = 1000

            time_surf = pygame.Surface((level.time / 2, 20))
            timer = time_surf.get_rect(center=(400, 30))
            pygame.draw.rect(screen, (0, 0, 100), timer)

            level.time -= 1

        # Update GUI
        gui.main_menu_manager.update(fps)
        gui.main_menu_manager.draw_ui(screen)

        pygame.display.flip()
        clock.tick(fps)
        print(clock.get_fps())

    pygame.quit()


def move_objects(x, y, level: Level):
    """Moves all walls and enemies in the level by (x,y)

    Args:
        x (int): amount to move objects by in x direction
        y (int): amount to move objects by in y direction
        level (Level): game level
    """
    for wall in level.wall_list:
        wall.move_ip(x, y)

    for enemy in level.enemy_list:
        enemy.rect.move_ip(x, y)

    for bullet in level.player_bullets:
        bullet.rect.move_ip(x, y)

    for bullet in level.enemy_bullets:
        bullet.rect.move_ip(x, y)

    level.origin_coords[0] += x
    level.origin_coords[1] += y


def move_player(level: Level, player: Player, pressed_keys):
    """Moves level around player on key press and handles wall collisions.

            Moves level around player to give illusion of player movement, and handles wall collisions.
            Movement speed is equal to player.speed.

            Args:
                level (Level): the level
                player (Player): the player character
                pressed_keys (bools): sequence of bools indicating which keys are pressed
            """
    wall_list = level.wall_list
    player_x = player.rect.x
    player_y = player.rect.y
    player_width = player.rect.width
    player_height = player.rect.height

    # Move walls in x direction
    if pressed_keys[pygame.K_a]:
        move_objects(player.speed, 0, level)

    if pressed_keys[pygame.K_d]:
        move_objects(-player.speed, 0, level)

    # Check collisions in x direction
    collision_index_x = player.rect.collidelistall(wall_list)

    if collision_index_x:

        for i in collision_index_x:
            wall_x = wall_list[i].x
            wall_width = wall_list[i].width

            if (player_x + player_width) > wall_x > player_x:
                move_objects((player_x + player_width - wall_x), 0, level)

            elif player_x < (wall_x + wall_width) < (player_x + player_width):
                move_objects(-(wall_x + wall_width - player_x), 0, level)

    # Move walls in y direction
    if pressed_keys[pygame.K_w]:
        move_objects(0, player.speed, level)

    if pressed_keys[pygame.K_s]:
        move_objects(0, -player.speed, level)

    # Check collisions in y direction
    collision_index_y = player.rect.collidelistall(wall_list)

    if collision_index_y:

        for i in collision_index_y:
            wall_y = wall_list[i].y
            wall_height = wall_list[i].height

            if (player_y + player_height) > wall_y > player_y:
                move_objects(0, (player_y + player_height - wall_y), level)

            elif player_y < (wall_y + wall_height) < (player_y + player_height):
                move_objects(0, -(wall_y + wall_height - player_y), level)


if __name__ == '__main__':
    main()
