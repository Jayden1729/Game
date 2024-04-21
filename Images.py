import pygame
import copy
import Level
import random


class Images:

    def __init__(self, square_size):

        # Tileset for background
        tile_images = pygame.image.load("sprites/TileSet.png")
        self.tileset = pygame.transform.scale(tile_images, (square_size * 30, square_size * 17))
        self.tile_dict = self.generate_tile_dict(square_size)

        # Explosion enemy images
        self.explosion_enemy_run = pygame.transform.scale2x(pygame.image.load("sprites/Droid Zapper/run.png"))
        self.ex_enemy_run_list = extract_sprite_animations(self.explosion_enemy_run, 6)
        self.explosion_enemy_death = pygame.image.load("sprites/Droid Zapper/damaged and death.png")
        self.ex_enemy_death_list = extract_sprite_animations(self.explosion_enemy_death, 8)


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

    def display_wall_images(self, level: Level, screen):
        """Displays walls on the screen.

        Args:
            level (Level): The game level.
            screen (pygame.display): The display window.
        """

        square_size = level.square_size

        for i in range(len(level.grid[0])):
            for j in range(len(level.grid)):
                if level.grid[j][i] == 1:
                    wall_type = get_wall_type([i, j], level.grid)
                    wall_rect = self.tile_dict[str(wall_type)]
                    screen.blit(self.tileset, (i * square_size + level.origin_coords[0],
                                               j * square_size + level.origin_coords[1]), wall_rect)

    def display_floor_images(self, level: Level, screen):
        """Displays floor images on the screen.

        Args:
            level (Level): The game level.
            screen (pygame.display): The display window.
        """

        square_size = level.square_size

        for i in range(len(level.floor_image_grid[0])):
            for j in range(len(level.floor_image_grid)):
                value = level.floor_image_grid[j][i]
                if value != ('n'):
                    floor_rect = self.tile_dict[str('floor_' + str(value))]
                    screen.blit(self.tileset, (i * square_size + level.origin_coords[0],
                                               j * square_size + level.origin_coords[1]), floor_rect)


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


def extract_sprite_animations(image_set, num_frames):
    """Extracts individual animation frames from png containing animation frames.

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
        frame_list.append(pygame.Rect((0, frame_height * (i - 1)), (image_width, frame_height)))

    return frame_list