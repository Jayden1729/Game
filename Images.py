import pygame
import copy
import Level
import random


class Images:

    def __init__(self, square_size):

        # Background images
        planet_image = pygame.image.load("sprites/planet03 downsized.png").convert_alpha()
        self.planet = pygame.transform.scale(planet_image, (500, 500))

        background_image = pygame.image.load("sprites/space_Background_1024.png").convert_alpha()
        self.background = background_image

        # Tileset for background
        tile_images = pygame.image.load("sprites/TileSet.png").convert_alpha()
        self.tileset = pygame.transform.scale(tile_images, (square_size * 30, square_size * 17))
        self.tile_dict = self.generate_tile_dict(square_size)

        # Bullets
        bullet_sf = 1.6

        self.red_bullet = pygame.transform.scale(
            pygame.image.load("sprites/Bullets/red bullet.png").convert_alpha(), (48, 15))
        self.red_bullet_list = extract_sprite_animations_horizontal(self.red_bullet, 3)

        self.purple_bullet = pygame.transform.scale(
            pygame.image.load("sprites/Bullets/purple bullet.png").convert_alpha(), (48 * bullet_sf, 15 * bullet_sf))
        self.purple_bullet_list = extract_sprite_animations_horizontal(self.purple_bullet, 3)

        self.green_bullet = pygame.transform.scale(
            pygame.image.load("sprites/Bullets/green bullet.png").convert_alpha(), (48 * bullet_sf, 15 * bullet_sf))
        self.green_bullet_list = extract_sprite_animations_horizontal(self.green_bullet, 3)

        # Normal enemy images
        self.normal_run = pygame.transform.scale2x(
            pygame.image.load("sprites/Bot Wheel/move with FX.png").convert_alpha())
        self.normal_run_list = extract_sprite_animations_vertical(self.normal_run, 8)
        self.normal_death = pygame.transform.scale2x(
            pygame.image.load("sprites/Bot Wheel/death.png").convert_alpha())
        self.normal_death_list = extract_sprite_animations_vertical(self.normal_death, 6)
        self.normal_hit = pygame.transform.scale2x(
            pygame.image.load("sprites/Bot Wheel/damaged.png").convert_alpha())
        self.normal_hit_list = extract_sprite_animations_vertical(self.normal_hit, 2)

        # Radial enemy images
        self.radial_run = pygame.transform.scale2x(
            pygame.image.load("sprites/stormhead/run.png").convert_alpha())
        self.radial_run_list = extract_sprite_animations_vertical(self.radial_run, 10)
        self.radial_death = pygame.transform.scale2x(
            pygame.image.load("sprites/stormhead/death.png").convert_alpha())
        self.radial_death_list = extract_sprite_animations_vertical(self.radial_death, 9)
        self.radial_hit = pygame.transform.scale2x(
            pygame.image.load("sprites/stormhead/damaged.png").convert_alpha())
        self.radial_hit_list = extract_sprite_animations_vertical(self.radial_hit, 2)

        # Melee enemy images
        mel_sf = 3
        self.melee_run = pygame.transform.scale(
            pygame.image.load("sprites/Mud Guard/Run.png").convert_alpha(), (82 * mel_sf, 138 * mel_sf))
        self.melee_run_list = extract_sprite_animations_vertical(self.melee_run, 6)
        self.melee_death = pygame.transform.scale(
            pygame.image.load("sprites/Mud Guard/damaged and death.png").convert_alpha(), (82 * mel_sf, 184 * mel_sf))
        self.melee_death_list = extract_sprite_animations_vertical(self.melee_death, 8)
        self.melee_attack = pygame.transform.scale(
            pygame.image.load("sprites/Mud Guard/attack 1.png").convert_alpha(), (82 * mel_sf, 161 * mel_sf))
        self.melee_attack_list = extract_sprite_animations_vertical(self.melee_attack, 7)

        # Explosion enemy images
        self.explosion_run = pygame.transform.scale2x(
            pygame.image.load("sprites/Droid Zapper/run.png").convert_alpha())
        self.explosion_run_list = extract_sprite_animations_vertical(self.explosion_run, 6)
        self.explosion_death = pygame.transform.scale2x(
            pygame.image.load("sprites/Droid Zapper/damaged and death.png").convert_alpha())
        self.explosion_death_list = extract_sprite_animations_vertical(self.explosion_death, 8)

        # Explosion images
        self.explosion_images = pygame.image.load("sprites/explosion-4.png").convert_alpha()
        self.explosion_list = extract_sprite_animations_horizontal(self.explosion_images, 12)


    def generate_tile_dict(self, square_size):
        """Generates a dictionary with the locations of each type of tile.

        Takes the tileset and sets self.tile_dict to a dictionary containing rects with the location of each type of
        tile in the tileset.
        """

        centre = pygame.Rect((11 * square_size, 7 * square_size), (square_size, square_size))

        right_centre = pygame.Rect((12 * square_size, 7 * square_size), (square_size, square_size))
        left_centre = pygame.Rect((10 * square_size, 7 * square_size), (square_size, square_size))
        top_centre = pygame.Rect((11 * square_size, 6 * square_size), (square_size, square_size))
        bot_centre = pygame.Rect((11 * square_size, 8 * square_size), (square_size, square_size))

        top_right_corner = pygame.Rect((12 * square_size, 6 * square_size), (square_size, square_size))
        top_left_corner = pygame.Rect((10 * square_size, 6 * square_size), (square_size, square_size))
        bot_right_corner = pygame.Rect((12 * square_size, 8 * square_size), (square_size, square_size))
        bot_left_corner = pygame.Rect((10 * square_size, 8 * square_size), (square_size, square_size))

        vertical_centre = pygame.Rect((14 * square_size, 7 * square_size), (square_size, square_size))
        horizontal_centre = pygame.Rect((17 * square_size, 8 * square_size), (square_size, square_size))

        bot_end = pygame.Rect((14 * square_size, 8 * square_size), (square_size, square_size))
        top_end = pygame.Rect((14 * square_size, 6 * square_size), (square_size, square_size))
        right_end = pygame.Rect((18 * square_size, 8 * square_size), (square_size, square_size))
        left_end = pygame.Rect((16 * square_size, 8 * square_size), (square_size, square_size))

        single = pygame.Rect((16 * square_size, 6 * square_size), (square_size, square_size))

        floor_0 = pygame.Rect((3 * square_size, 12 * square_size), (square_size, square_size))
        floor_1 = pygame.Rect((3 * square_size, 10 * square_size), (square_size, square_size))
        floor_2 = pygame.Rect((4 * square_size, 10 * square_size), (square_size, square_size))
        floor_3 = pygame.Rect((3 * square_size, 11 * square_size), (square_size, square_size))
        floor_4 = pygame.Rect((4 * square_size, 11 * square_size), (square_size, square_size))

        return {'centre': centre, 'right_centre': right_centre, 'left_centre': left_centre,
                'top_centre': top_centre, 'bot_centre': bot_centre, 'top_right_corner': top_right_corner,
                'top_left_corner': top_left_corner, 'bot_right_corner': bot_right_corner,
                'bot_left_corner': bot_left_corner, 'vertical_centre': vertical_centre,
                'horizontal_centre': horizontal_centre, 'bot_end': bot_end, 'top_end': top_end,
                'right_end': right_end, 'left_end': left_end, 'single': single, 'floor_0': floor_0, 'floor_1': floor_1,
                'floor_2': floor_2, 'floor_3': floor_3, 'floor_4': floor_4}

    def display_wall_images(self, level: Level, screen, screen_width, screen_height):
        """Displays walls on the screen.

        Does not show walls if they are outside the display window.

        Args:
            level (Level): The game level.
            screen (pygame.display): The display window.
            screen_width(int): the screen width.
            screen_height(int): the screen height.
        """

        square_size = level.square_size

        for i in range(len(level.grid[0])):
            for j in range(len(level.grid)):
                if level.grid[j][i] == 1:
                    wall_x = i * square_size + level.origin_coords[0]
                    wall_y = j * square_size + level.origin_coords[1]

                    if wall_x < screen_width and wall_y < screen_height:
                        wall_type = get_wall_type([i, j], level.grid)
                        wall_rect = self.tile_dict[str(wall_type)]
                        screen.blit(self.tileset, (wall_x, wall_y), wall_rect)

    def display_floor_images(self, level: Level, screen, screen_width, screen_height):
        """Displays floor images on the screen.

        Does not display the floor outside the visible display area.

        Args:
            level (Level): The game level.
            screen (pygame.display): The display window.
            screen_width(int): the screen width.
            screen_height(int): the screen height.
        """

        square_size = level.square_size

        for i in range(len(level.floor_image_grid[0])):
            for j in range(len(level.floor_image_grid)):
                floor_x = i * square_size + level.origin_coords[0]
                floor_y = j * square_size + level.origin_coords[1]

                if floor_x < screen_width and floor_y < screen_height:
                    value = level.floor_image_grid[j][i]
                    if value != ('n'):
                        floor_rect = self.tile_dict[str('floor_' + str(value))]
                        screen.blit(self.tileset, (floor_x, floor_y), floor_rect)

def get_wall_type(wall, grid):
    """Determines the type of wall connector to display.

    Args:
        wall (List[int]): a list [x, y] of the position of a wall in the grid.
        grid (List[List[int,str]]): a 2D list of ints and strings.

    Returns:
        str: a string describing the type of wall connector to display.
    """
    x = wall[0]
    y = wall[1]

    # Check if surrounding grid squares are walls
    left = False
    right = False
    top = False
    bot = False

    if x - 1 < 0:
        left = False
    if grid[y][x - 1] == 1:
        left = True

    if x + 1 >= len(grid[0]):
        right = False
    if grid[y][x + 1] == 1:
        right = True

    if y - 1 < 0:
        top = False
    if grid[y - 1][x] == 1:
        top = True

    if y + 1 >= len(grid[0]):
        bot = False
    if grid[y + 1][x] == 1:
        bot = True

    # Determine wall type

    if top and bot and left and right:
        return 'centre'
    if top and left and bot:
        return 'right_centre'
    if top and right and bot:
        return 'left_centre'
    if left and bot and right:
        return 'top_centre'
    if left and top and right:
        return 'bot_centre'
    if right and bot:
        return 'top_left_corner'
    if left and bot:
        return 'top_right_corner'
    if right and top:
        return 'bot_left_corner'
    if left and top:
        return 'bot_right_corner'
    if top and bot:
        return 'vertical_centre'
    if left and right:
        return 'horizontal_centre'
    if top:
        return 'bot_end'
    if bot:
        return 'top_end'
    if left:
        return 'right_end'
    if right:
        return 'left_end'

    return 'single'


def extract_sprite_animations_vertical(image_set, num_frames):
    """Extracts individual animation frames from png containing animation frames arranged vertically.

    Args:
        image_set (.png): a png file containing the frames of animation in a vertical arrangement.
        num_frames (int): the number of frames in the full animation.

    Returns:
        List[pygame.Rect]: a list of pygame.Rect objects that specify the location of each frame of the animation in the
            image_set.

    """
    image_width = image_set.get_width()
    image_height = image_set.get_height()
    frame_height = image_height / num_frames

    frame_list = []

    for i in range(num_frames):
        frame_list.append(pygame.Rect((0, frame_height * (i)), (image_width, frame_height)))

    return frame_list

def extract_sprite_animations_horizontal(image_set, num_frames):
    """Extracts individual animation frames from png containing animation frames arranged horizontally.

    Args:
        image_set (.png): a png file containing the frames of animation in a horizontal arrangement.
        num_frames (int): the number of frames in the full animation.

    Returns:
        List[pygame.Rect]: a list of pygame.Rect objects that specify the location of each frame of the animation in the
            image_set.

    """
    image_width = image_set.get_width()
    image_height = image_set.get_height()
    frame_width = image_width / num_frames

    frame_list = []

    for i in range(num_frames):
        frame_list.append(pygame.Rect((frame_width * (i), 0), (frame_width, image_height)))

    return frame_list
