"""Player class controls attributes of the player character

"""
import pygame
import Level
import Bullet
import Images
import math
import copy


class Player(pygame.sprite.Sprite):

    def __init__(self, player_dict, screen_dimensions):
        """
        Initialises the Player class.
        """
        super(Player, self).__init__()

        self.torso_images = player_dict['torso']
        self.legs_images = player_dict['legs']

        rect_size = 20
        self.x = round(screen_dimensions[0] / 2)
        self.y = round(screen_dimensions[1] / 2)
        self.surf = pygame.Surface((rect_size, rect_size))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.vector2 = pygame.math.Vector2(self.x, self.y)
        self.speed = 5
        self.projectile_speed = 10
        self.attack_cooldown = 0

        self.is_moving = False
        self.is_shooting = False
        self.legs_frame = 0
        self.legs_frame_break = 0
        self.torso_frame = 0
        self.torso_frame_break = 0

    def attack(self, player_bullets, screen_width, screen_height, bullet_dict):
        """Creates a bullet and adds to player_bullets group.

        Args:
            player_bullets (pygame.Group[Bullets]): a pygame.Group object of Bullet objects.
            screen_width (int): the screen width.
            screen_height (int): the screen height.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_vector = pygame.math.Vector2(mouse_x, mouse_y)

        try:
            mouse_angle = math.degrees(math.atan((mouse_y - screen_height / 2) / abs((mouse_x - screen_width / 2))))
        except ZeroDivisionError:
            mouse_angle = 0

        gun_vector = copy.deepcopy(self.vector2)
        flip = 1

        if mouse_x < screen_width / 2:
            flip = -1

        if mouse_angle <= -50:
            gun_vector.x += 10 * flip
            gun_vector.y += -38
        elif mouse_angle <= -15:
            gun_vector.x += 26 * flip
            gun_vector.y += -28
        elif mouse_angle >= 50:
            gun_vector.x += 20 * flip
            gun_vector.y += 25
        elif mouse_angle >= 15:
            gun_vector.x += 29 * flip
            gun_vector.y += 7
        else:
            gun_vector.x += 30 * flip
            gun_vector.y += -12

        bullet_vector = mouse_vector - gun_vector

        player_bullets.add(Bullet.Bullet(gun_vector.x, gun_vector.y, bullet_vector, self.projectile_speed, bullet_dict['red']))
        self.attack_cooldown = 20
        self.is_shooting = True
        self.torso_frame_break = 0
        self.torso_frame = 0

    def move(self, level: Level, pressed_keys):
        """Moves level around player on key press and handles wall collisions.

        Moves level around player to give illusion of player movement, and handles wall collisions.
        Movement speed is equal to self.speed.

        Args:
            level (Level): the level
            pressed_keys (bools): sequence of bools indicating which keys are pressed
        """
        moving = False
        wall_list = level.wall_list
        player_x = self.rect.x
        player_y = self.rect.y
        player_width = self.rect.width
        player_height = self.rect.height

        # Move walls in x direction
        if pressed_keys[pygame.K_a]:
            move_objects(self.speed, 0, level)
            moving = True

        if pressed_keys[pygame.K_d]:
            move_objects(-self.speed, 0, level)
            moving = True

        # Check collisions in x direction
        collision_index_x = self.rect.collidelistall(wall_list)

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
            move_objects(0, self.speed, level)
            moving = True

        if pressed_keys[pygame.K_s]:
            move_objects(0, -self.speed, level)
            moving = True

        # Check collisions in y direction
        collision_index_y = self.rect.collidelistall(wall_list)

        if collision_index_y:

            for i in collision_index_y:
                wall_y = wall_list[i].y
                wall_height = wall_list[i].height

                if (player_y + player_height) > wall_y > player_y:
                    move_objects(0, (player_y + player_height - wall_y), level)

                elif player_y < (wall_y + wall_height) < (player_y + player_height):
                    move_objects(0, -(wall_y + wall_height - player_y), level)

        # Update if player is moving
        self.is_moving = moving

    def animate(self, screen):
        """Plays the player animation.

        Args:
            screen (pygame.display): the game screen.
        """
        direction = 1
        frame_break = 7

        mouse_pos = pygame.mouse.get_pos()

        try:
            mouse_angle = math.degrees(
                math.atan((mouse_pos[1] - self.y) / abs((mouse_pos[0] - self.x))))
        except ZeroDivisionError:
            mouse_angle = 0

        # Get torso shooting angle sprites
        if mouse_angle <= -50:
            torso_list = self.torso_images['shoot_up_60']

        elif mouse_angle <= -15:
            torso_list = self.torso_images['shoot_up_30']

        elif mouse_angle >= 50:
            torso_list = self.torso_images['shoot_down_60']

        elif mouse_angle >= 15:
            torso_list = self.torso_images['shoot_down_30']

        else:
            torso_list = self.torso_images['shoot_forward']

        torso_sprites = torso_list[0]
        torso_frames = torso_list[1]
        torso_offset = torso_list[2]

        # Get legs sprites
        if self.is_moving:
            legs_list = self.legs_images['run']
        else:
            legs_list = self.legs_images['idle']

        legs_sprites = legs_list[0]
        legs_frames = legs_list[1]
        legs_offset = legs_list[2]

        # Check if animation has reached the end
        if self.legs_frame >= len(legs_frames):
            self.legs_frame = 0

        if self.torso_frame >= len(torso_frames):
            self.torso_frame = 0
            self.is_shooting = False

        # Flip images if mouse is left of the player
        if mouse_pos[0] < self.x:
            legs_sprites = pygame.transform.flip(legs_sprites, True, False)
            torso_sprites = pygame.transform.flip(torso_sprites, True, False)
            direction = -1

        if self.is_shooting:
            torso_animation_frame = direction * self.torso_frame - int((1 - direction) / 2)
        else:
            torso_animation_frame = - int((1 - direction) / 2)

        # Blit images to screen
        screen.blit(legs_sprites, (self.rect.x - legs_offset[0], self.rect.y - legs_offset[1]),
                    legs_frames[direction * self.legs_frame])

        screen.blit(torso_sprites, (self.rect.x - torso_offset[0], self.rect.y - torso_offset[1]),
                    torso_frames[torso_animation_frame])

        if self.legs_frame_break == 0:
            self.legs_frame += 1
            self.legs_frame_break = frame_break
        else:
            self.legs_frame_break -= 1

        if self.torso_frame_break == 0:
            self.torso_frame += 1
            self.torso_frame_break = 4
        else:
            self.torso_frame_break -= 1


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
