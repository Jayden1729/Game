"""Player class controls attributes of the player character

"""
import pygame
import Level
import Bullet


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

        self.grid_x = None
        self.grid_y = None

        self.sprite = pygame.image.load("sprites/Player_sprite.png")
        self.sprite = pygame.transform.scale(self.sprite, (64, 64))


    def attack(self, player_bullets):
        """Creates a bullet and adds to player_bullets group

        Args:
            player_bullets (pygame.Group[Bullets]): a pygame.Group object of Bullet objects.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_vector = pygame.math.Vector2(mouse_x, mouse_y)

        bullet_vector = mouse_vector - self.vector2

        player_bullets.add(Bullet.Bullet(400, 400, bullet_vector, self.projectile_speed))
        self.attack_cooldown = 20

    def move(self, level: Level, pressed_keys):
        """Moves level around player on key press and handles wall collisions.

                Moves level around player to give illusion of player movement, and handles wall collisions.
                Movement speed is equal to self.speed.

                Args:
                    level (Level): the level
                    pressed_keys (bools): sequence of bools indicating which keys are pressed
                """
        wall_list = level.wall_list
        player_x = self.rect.x
        player_y = self.rect.y
        player_width = self.rect.width
        player_height = self.rect.height

        # Move walls in x direction
        if pressed_keys[pygame.K_a]:
            move_objects(self.speed, 0, level)

        if pressed_keys[pygame.K_d]:
            move_objects(-self.speed, 0, level)

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

        if pressed_keys[pygame.K_s]:
            move_objects(0, -self.speed, level)

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
