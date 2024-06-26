import pygame
import Level
import os
import configparser
import json


class Images:

    def __init__(self, min_dimension):

        square_size = min_dimension / 16

        # Background images
        planet_image = pygame.image.load("sprites/other/background/planet_downsized.png").convert_alpha()
        self.planet = pygame.transform.scale(planet_image, (500, 500))

        background_image = pygame.image.load("sprites/other/background/background_1024.png").convert_alpha()
        self.background = background_image

        # Tileset for background
        tile_images = pygame.image.load("sprites/other/level/tileset.png").convert_alpha()
        self.tileset = pygame.transform.scale(tile_images, (square_size * 30, square_size * 17))
        self.tile_dict = self.generate_tile_dict(square_size)

        # Bullets
        bullet_sf = 1.6 * min_dimension / 800

        self.image_dict = get_images(min_dimension)
        self.enemy_dict = self.image_dict['enemy']
        self.player_dict = self.image_dict['player']
        self.other_dict = self.image_dict['other']
        self.bullet_dict = self.other_dict['bullet']

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


def get_images(min_dimension):
    """Generates a dictionary of all images in the sprites folder.

    Args:
        min_dimension (int): the minimum screen dimension.

    Returns:
        {str, {str, {str, [pygame.image, [pygame.Rect]]}}}: a 3-layer dictionary representing the sprites folder
            structure. The final level contains a key with a list for each image. The list contains the image as element
            [0], a list of pygame.Rect objects specifying the location of each animation frame on the image as
            element [1], a list [x,y] containing the left_offset of the image as element [2], and a list [x,y]
            containing the right_offset of the image as element [3].
    """
    image_dict = {}

    for folder in os.scandir('sprites'):
        folder_name = os.path.splitext(os.path.basename(folder))[0]

        images = configparser.SafeConfigParser()
        images.read(f'sprites/{folder_name}/{folder_name}_images.ini')

        folder_dict = {}

        for child_folder in os.scandir(f'sprites/{folder_name}'):
            child_folder_name = os.path.splitext(os.path.basename(child_folder))[0]

            if child_folder_name == f'{folder_name}_images':
                continue

            new_dict = {}
            config = dict(images.items(child_folder_name))

            try:
                folder_scale_factor = json.loads(config['scale_factor']) * min_dimension / 800
            except:
                print(f'Scale factor is not specified for {child_folder_name}')
                folder_scale_factor = 1

            try:
                folder_axis = config['axis']
            except:
                print(f'Axis is not specified for {child_folder_name}')
                folder_axis = 'vertical'

            try:
                folder_left_offset = json.loads(config['left_offset'])
                folder_right_offset = json.loads(config['right_offset'])
            except:
                print(f'Scale factor is not specified for {child_folder_name}')
                folder_left_offset = [0, 0]
                folder_right_offset = [0, 0]

            for image_set in os.scandir(f'sprites/{folder_name}/{child_folder_name}'):
                image_name = os.path.splitext(os.path.basename(image_set))[0]
                image_extension = os.path.splitext(os.path.basename(image_set))[1]

                if image_extension != '.png':
                    continue

                try:
                    override = configparser.SafeConfigParser()
                    override.read(f'sprites/{folder_name}/{child_folder_name}/{image_name}_override.ini')
                    override_config = dict(override.items(f'{image_name}'))
                    axis = override_config['axis']
                    scale_factor = json.loads(override_config['scale_factor']) * min_dimension / 800
                    left_offset = json.loads(override_config['left_offset'])
                    right_offset = json.loads(override_config['right_offset'])
                except:
                    axis = folder_axis
                    scale_factor = folder_scale_factor * min_dimension / 800
                    left_offset = folder_left_offset
                    right_offset = folder_right_offset

                try:
                    num_frames = json.loads(config[image_name])
                except:
                    print(f'Number of image frames not specified for {image_name} in {child_folder_name}')
                    continue

                load_images = pygame.transform.scale_by(
                    pygame.image.load(f'sprites/{folder_name}/{child_folder_name}/{image_name}.png').convert_alpha(),
                    scale_factor)

                if axis == 'horizontal':
                    image_frames = extract_sprite_animations_horizontal(load_images, num_frames)
                else:
                    image_frames = extract_sprite_animations_vertical(load_images, num_frames)

                left_offset = scale_list(left_offset, min_dimension)
                right_offset = scale_list(right_offset, min_dimension)
                print(left_offset, right_offset)

                new_dict.update({image_name: [load_images, image_frames, left_offset, right_offset]})

            folder_dict.update({child_folder_name: new_dict})

        image_dict.update({folder_name: folder_dict})

    return image_dict

def scale_list(list, min_dimension):
    '''Scales a list by the min_dimension.

    Args:
        list (List[ints]): a list of ints.
        min_dimension (int): the minimum screen dimension.

    Returns:
        List[ints]: a list of ints scaled by the min_dimension.
    '''

    for i in range(len(list)):
        list[i] = round(list[i] / 800 * min_dimension)

    return list