"""Player class controls attributes of the player character

"""
import pygame
import Level
import Bullet
import Images
import math
import copy

class Player(pygame.sprite.Sprite):

    def __init__(self):
        """
        Initialises the Player class.
        """
        super(Player, self).__init__()
        rect_size = 20
        self.surf = pygame.Surface((rect_size, rect_size))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(400, 400))
        self.vector2 = pygame.math.Vector2(400, 400)
        self.speed = 5
        self.projectile_speed = 10
        self.attack_cooldown = 0

        self.is_moving = False
        self.is_shooting = False
        self.torso_frame = 0
        self.legs_frame = 0
        self.legs_frame_break = 0
        self.torso_frame_break = 0
        self.shooting_frame = 0
        self.shooting_frame_break = 0

        scale_factor = 1.3
        self.player_torso_idle = pygame.transform.scale(
            pygame.image.load("sprites/Player/Torso/torso idle.png").convert_alpha(), (200 * scale_factor, 50 * scale_factor))
        self.player_torso_idle_list = Images.extract_sprite_animations_horizontal(self.player_torso_idle, 4)

        self.player_torso_shoot = pygame.transform.scale(
            pygame.image.load("sprites/Player/Torso/Shoot.png").convert_alpha(), (320 * scale_factor, 50 * scale_factor))
        self.player_torso_shoot_list = Images.extract_sprite_animations_horizontal(self.player_torso_shoot, 4)

        self.player_torso_shoot_down_30 = pygame.transform.scale(
            pygame.image.load("sprites/Player/Torso/Shoot down.png").convert_alpha(),
            (320 * scale_factor, 50 * scale_factor))
        self.player_torso_shoot_down_30_list = Images.extract_sprite_animations_horizontal(self.player_torso_shoot_down_30, 4)

        self.player_torso_shoot_down_60 = pygame.transform.scale(
            pygame.image.load("sprites/Player/Torso/shoot down 60.png").convert_alpha(),
            (320 * scale_factor, 100 * scale_factor))
        self.player_torso_shoot_down_60_list = Images.extract_sprite_animations_horizontal(self.player_torso_shoot_down_60, 4)

        self.player_torso_shoot_up_30 = pygame.transform.scale(
            pygame.image.load("sprites/Player/Torso/shoot up 30.png").convert_alpha(),
            (320 * scale_factor, 100 * scale_factor))
        self.player_torso_shoot_up_30_list = Images.extract_sprite_animations_horizontal(self.player_torso_shoot_up_30, 4)

        self.player_torso_shoot_up_60 = pygame.transform.scale(
            pygame.image.load("sprites/Player/Torso/shoot up 60.png").convert_alpha(),
            (320 * scale_factor, 100 * scale_factor))
        self.player_torso_shoot_up_60_list = Images.extract_sprite_animations_horizontal(self.player_torso_shoot_up_60, 4)

        self.player_legs_idle = pygame.transform.scale(
            pygame.image.load("sprites/Player/Legs/leg_idle.png").convert_alpha(), (50 * scale_factor, 50 * scale_factor))
        self.player_legs_idle_list = Images.extract_sprite_animations_horizontal(self.player_legs_idle, 1)

        self.player_legs_run = pygame.transform.scale(
            pygame.image.load("sprites/Player/Legs/Leg run.png").convert_alpha(), (400 * scale_factor, 50 * scale_factor))
        self.player_legs_run_list = Images.extract_sprite_animations_horizontal(self.player_legs_run, 8)


    def attack(self, player_bullets, screen_width, screen_height):
        """Creates a bullet and adds to player_bullets group.

        Args:
            player_bullets (pygame.Group[Bullets]): a pygame.Group object of Bullet objects.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_vector = pygame.math.Vector2(mouse_x, mouse_y)

        try:
            mouse_angle = math.degrees(math.atan((mouse_y-screen_height/2)/abs((mouse_x-screen_width/2))))
        except ZeroDivisionError:
            mouse_angle = 0

        gun_vector = copy.deepcopy(self.vector2)
        flip = 1

        if mouse_x < screen_width/2:
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

        player_bullets.add(Bullet.Bullet(gun_vector.x, gun_vector.y, bullet_vector, self.projectile_speed, 'red'))
        self.attack_cooldown = 20
        self.is_shooting = True
        self.shooting_frame_break = 0
        self.shooting_frame = 0

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

    def run_animation(self, screen, screen_width, screen_height):
        """Plays the player animation.

        Args:
            screen (pygame.display): the game screen.
            screen_width (int): the width of the screen.
            screen_height (int): the height of the screen.
        """
        offset = [23, 25]
        torso_offset = [42, 25]
        shooting_offset = [42, 63]
        frame_break = 7

        mouse_pos = pygame.mouse.get_pos()

        try:
            mouse_angle = math.degrees(math.atan((mouse_pos[1]-screen_height/2)/abs((mouse_pos[0]-screen_width/2))))
        except ZeroDivisionError:
            mouse_angle = 0

        if mouse_angle <= -50:
            shooting_images = self.player_torso_shoot_up_60
            shooting_list = self.player_torso_shoot_up_60_list
            torso_offset = shooting_offset
        elif mouse_angle <= -15:
            shooting_images = self.player_torso_shoot_up_30
            shooting_list = self.player_torso_shoot_up_30_list
            torso_offset = shooting_offset
        elif mouse_angle >= 50:
            shooting_images = self.player_torso_shoot_down_60
            shooting_list = self.player_torso_shoot_down_60_list
            torso_offset = shooting_offset
        elif mouse_angle >= 15:
            shooting_images = self.player_torso_shoot_down_30
            shooting_list = self.player_torso_shoot_down_30_list
            shooting_offset = torso_offset
        else:
            shooting_images = self.player_torso_shoot
            shooting_list = self.player_torso_shoot_list
            shooting_offset = torso_offset

        torso_images = shooting_images
        torso_list = shooting_list[0:1]

        if self.is_moving:
            legs_images = self.player_legs_run
            legs_list = self.player_legs_run_list
        else:
            legs_images = self.player_legs_idle
            legs_list = self.player_legs_idle_list

        if self.legs_frame >= len(legs_list):
            self.legs_frame = 0

        if self.torso_frame >= len(torso_list):
            self.torso_frame = 0

        if self.shooting_frame >= len(shooting_list):
            self.shooting_frame = 0
            self.is_shooting = False

        if mouse_pos[0] < screen_width/2:
            legs_images = pygame.transform.flip(legs_images, True, False)
            screen.blit(legs_images, (self.rect.x - offset[0], self.rect.y - offset[1]),
                        legs_list[self.legs_frame])

            if self.is_shooting:
                shooting_images = pygame.transform.flip(shooting_images, True, False)
                screen.blit(shooting_images, (self.rect.x - shooting_offset[0], self.rect.y - shooting_offset[1]),
                            shooting_list[-self.shooting_frame - 1])
            else:
                torso_images = pygame.transform.flip(torso_images, True, False)
                screen.blit(torso_images, (self.rect.x - torso_offset[0], self.rect.y - torso_offset[1]),
                            shooting_list[-1])
        else:
            screen.blit(legs_images, (self.rect.x - offset[0], self.rect.y - offset[1]),
                        legs_list[self.legs_frame])

            if self.is_shooting:
                screen.blit(shooting_images, (self.rect.x - shooting_offset[0], self.rect.y - shooting_offset[1]),
                            shooting_list[self.shooting_frame])
            else:
                screen.blit(torso_images, (self.rect.x - torso_offset[0], self.rect.y - torso_offset[1]),
                            torso_list[self.torso_frame])

        if self.legs_frame_break == 0:
            self.legs_frame += 1
            self.legs_frame_break = frame_break
        else:
            self.legs_frame_break -= 1

        if self.torso_frame_break == 0:
            self.torso_frame += 1
            self.torso_frame_break = frame_break
        else:
            self.torso_frame_break -= 1

        if self.shooting_frame_break == 0:
            self.shooting_frame += 1
            self.shooting_frame_break = 4
        else:
            self.shooting_frame_break -= 1




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
