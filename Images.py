import pygame
import copy


class Images():

    def __init__(self, screen):
        self.tileset = pygame.image.load("sprites/TileSet.png")
        self.tile_dict = self.generate_tile_dict(screen)

    def generate_tile_dict(self):
        """Generates a dictionary with the locations of each type of tile.

        Takes the tileset and sets self.tile_dict to a dictionary containing rects with the location of each type of
        tile in the tileset.
        """
        tile_width = self.tileset.get_width() / 30
        tile_height = self.tileset.get_height() / 17
        print(tile_height, tile_width)

        centre = pygame.Rect((11 * tile_height, 7 * tile_height), (tile_width, tile_height))

        right_centre = pygame.Rect((12 * tile_height, 7 * tile_height), (tile_width, tile_height))

        left_centre = pygame.Rect((10 * tile_height, 7 * tile_height), (tile_width, tile_height))

        top_centre = pygame.Rect((11 * tile_height, 6 * tile_height), (tile_width, tile_height))

        bot_centre = pygame.Rect((11 * tile_height, 8 * tile_height), (tile_width, tile_height))

        top_right_corner = pygame.Rect((12 * tile_height, 6 * tile_height), (tile_width, tile_height))

        top_left_corner = pygame.Rect((10 * tile_height, 6 * tile_height), (tile_width, tile_height))

        bot_right_corner = pygame.Rect((12 * tile_height, 8 * tile_height), (tile_width, tile_height))

        bot_left_corner = pygame.Rect((10 * tile_height, 8 * tile_height), (tile_width, tile_height))

        vertical_centre = pygame.Rect((14 * tile_height, 7 * tile_height), (tile_width, tile_height))

        horizontal_centre = pygame.Rect((17 * tile_height, 8 * tile_height), (tile_width, tile_height))

        bot_end = pygame.Rect((14 * tile_height, 8 * tile_height), (tile_width, tile_height))

        top_end = pygame.Rect((14 * tile_height, 6 * tile_height), (tile_width, tile_height))

        right_end = pygame.Rect((18 * tile_height, 8 * tile_height), (tile_width, tile_height))

        left_end = pygame.Rect((16 * tile_height, 8 * tile_height), (tile_width, tile_height))

        single = pygame.Rect((16 * tile_height, 6 * tile_height), (tile_width, tile_height))

        self.tile_dict = {'centre': centre, 'right_centre': right_centre, 'left_centre': left_centre,
                          'top_centre': top_centre, 'bot_centre': bot_centre, 'top_right_corner': top_right_corner,
                          'top_left_corner': top_left_corner, 'bot_right_corner': bot_right_corner,
                          'bot_left_corner': bot_left_corner, 'vertical_centre': vertical_centre,
                          'horizontal_centre': horizontal_centre, 'bot_end': bot_end, 'top_end': top_end,
                          'right_end': right_end, 'left_end': left_end, 'single': single}

    def level_images(self, level):

        new_grid = copy.deepcopy(level.grid)

        for i in range(len(new_grid[0])):
            for j in range(len(new_grid)):
                if new_grid[j][i] == 1:
                    wall_type = get_wall_type([i, j], level.grid)
                    new_grid[j][i] = wall_type

        print(new_grid)


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

    # Determine correct wall image

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
