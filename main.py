# -*- coding: utf-8 -*-
"""
Naming conventions:

class: CapWords
variable: lower_case
constants: CAPITAL_CASE



"""

import pygame
import csv
import Player
import Level
import Bullet


def main():
    # initialise pygame
    pygame.init()

    # Variables
    screen_width = 800
    screen_height = 800
    fps = 90

    # Setup initial objects
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    player = Player.Player()

    with open('Game_grid.csv') as csvfile:
        reader = csv.reader(csvfile)
        game_grid = list(reader)
        for i in range(len(game_grid)):
            for j in range(len(game_grid[0])):
                if game_grid[i][j] == '1':
                    game_grid[i][j] = 1

    level = Level.Level(game_grid, 80)

    running = True

    # Game Loop
    while running:
        # Fill screen background
        screen.fill((90, 90, 90))

        # Get all pressed keys
        pressed_keys = pygame.key.get_pressed()

        # for loop through event queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            # Check if player is attacking
            elif (event.type == pygame.MOUSEBUTTONDOWN or pressed_keys[pygame.K_SPACE]) and player.attack_cooldown == 0:
                player.attack(level.player_bullets)

        # Draw walls on screen
        for wall in level.wall_list:
            pygame.draw.rect(screen, (0, 150, 0), wall)

        # Determine enemy movement and draw them on screen
        for enemy in level.enemy_list:
            enemy.update_movement(level, player, 1.5, 5)
            screen.blit(enemy.surf, enemy.rect)
            enemy.attack(level)


        # Draw and move player bullets + check collisions
        for bullet in level.player_bullets:
            bullet.rect.move_ip(bullet.vector.x * bullet.speed, bullet.vector.y * bullet.speed)
            if bullet.rect.collidelistall(level.wall_list):
                bullet.kill()

            for enemy in level.enemy_list:
                if pygame.Rect.colliderect(bullet.rect, enemy.rect):
                    bullet.kill()
                    enemy.kill()

            screen.blit(bullet.surf, bullet.rect)

        # Draw and move enemy bullets + check collisions
        for bullet in level.enemy_bullets:
            bullet.rect.move_ip(bullet.vector.x * bullet.speed, bullet.vector.y * bullet.speed)
            if bullet.rect.collidelistall(level.wall_list):
                bullet.kill()

            if pygame.Rect.colliderect(player.rect, bullet.rect):
                player.hp -= 10
                bullet.kill()

            screen.blit(bullet.surf, bullet.rect)

        # Player movement and draw player
        move_player(level, player, pressed_keys)
        screen.blit(player.surf, player.rect)

        # Reduce player attack cooldown
        if player.attack_cooldown > 0:
            player.attack_cooldown -= 1

        pygame.display.flip()
        clock.tick(fps)

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

    level.origin_coords.x += x
    level.origin_coords.y += y


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
