from moviepy import *
import random
import itertools

black = (0, 0, 0)
white = (255, 255, 255)

screen_size = (1080, 1920)

x_coords = [x for x in range(25, 826, 400)]
y_coords = [y for y in range(950, 1551, 200)]
scrapbook_positions = list(itertools.product(x_coords, y_coords))

def human_format(num: int):
    """
    This function takes in a number and returns a formatted string with magnitude noted as a letter.
    :param num: The number to convert (e.g. 15000000)
    :return: Formatted string (e.g. 15M)
    """
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '$' + '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def create_background_clip(clip_size: tuple, bg_color: tuple, fps: int):
    """
    This function produces a single clip with a solid background color.
    :param clip_size: The width and height of the clip
    :param bg_color: The color to use for the background
    :param fps: The desired FPS for the clip
    :return: MoviePy ColorClip with the given parameters
    """
    bg_clip = ColorClip(size=clip_size, color=bg_color).with_fps(fps)
    return bg_clip

def image_scrapbook_clip(filepath: str, duration: int, fade_in: float, fade_out: float, position: tuple, deg_rotated: int):
    """
    This function produces a single clip of a rotated image that fades in and out on a certain point on the screen.


    :param filepath: The filepath for the desired image
    :param duration: The duration (in seconds) that the image will stay on screen
    :param fade_in: The duration (in seconds) of the fade in effect
    :param fade_out: The duration (in seconds) of the fade out effect
    :param position: The coordinates for where the image will appear on screen
    :param deg_rotated: Degrees of rotation applied to the image
    :return: MoviePy ImageClip with the given parameters
    """
    scrapbook_clip = (ImageClip(filepath)
                      .with_duration(duration)
                      .with_effects([vfx.CrossFadeIn(fade_in).copy(), vfx.CrossFadeOut(fade_out).copy()])
                      .with_position(position)
                      .with_effects([vfx.Rotate(deg_rotated).copy(), vfx.Resize(width=540).copy()])
                     )
    return scrapbook_clip

def all_scrapbook_clips(full_duration: int, start_time: int, photo_list: list):
    """
    This function produces a list of image clips with randomized locations and degree of rotation.
    The number of image clips is determined by the duration passed.


    :param full_duration: The duration of the full clip that the scrapbook photos will overlap with
    :param start_time: Time (in seconds) to start the sequence of scrapbook photos
    :param photo_list: List of filepaths to use
    :return: List of randomly generated MoviePy ImageClips
    """
    scrapbook_clips = []
    used_coords = []
    used_pics = []
    for i in range(int(full_duration / 4) - 1):
        print('\nClip', i)

        scrap_start = (i * 4) + 1
        print('Start', scrap_start)

        scrap_duration = ((full_duration - 1) - scrap_start)
        if (scrap_start + scrap_duration) > (full_duration - 1):
            scrap_duration = ((full_duration - 1) - scrap_start)
        print('Duration', scrap_duration)

        random_position = random.choice(scrapbook_positions)
        while random_position in used_coords:
            random_position = random.choice(scrapbook_positions)
        used_coords.append(random_position)
        random_rotation = random.choice(range(-30, 30, 1))
        print(random_position, random_rotation)

        random_photo = random.choice(photo_list)
        while random_photo in used_pics:
            random_photo = random.choice(photo_list)
        used_pics.append(random_photo)
        scrapbook_clips.append(image_scrapbook_clip(filepath=random_photo,
                                                    duration=scrap_duration, fade_in=0.5, fade_out=1.0,
                                                    position=random_position, deg_rotated=random_rotation)
                               .with_start(scrap_start+start_time))
    return scrapbook_clips

def create_text_clip(clip_size: tuple, font_filepath: str, font_size: int, text_color: tuple, text_block: str):
    """
    This function produces a single text clip with the text centered.
    Intended for most blocks of text in Wrapped.
    :param clip_size: The width and height of the clip
    :param font_filepath: Filepath for font file
    :param font_size: Size of font
    :param text_color: Color of font
    :param text_block: String of text to use as content of clip
    :return: MoviePy TextClip with given parameters
    """
    starting_clip = TextClip(size = clip_size,
                             font = font_filepath,
                             font_size = font_size,
                             text = text_block,
                             color = text_color,
                             text_align = 'center',
                             vertical_align = 'center',
                             interline = 8
                            ).with_position(('center', 'center'))
    return starting_clip

def create_num_clip(clip_size: tuple, font_filepath: str, font_size: int, text_color: tuple, num: str):
    """
    This function produces a single text clip with slightly different spacing from create_text_clip().
    Intended for numerical sliding blocks of texts in Wrapped.
    :param clip_size: The width and height of the clip
    :param font_filepath: Filepath for font file
    :param font_size: Size of font
    :param text_color: Color of font
    :param num: String of text to use as content (should be a number)
    :return: MoviePy TextClip with given parameters
    """
    num_clip = TextClip(size = clip_size,
                        font = font_filepath,
                        font_size = font_size,
                        text = '\n'+num+'\n',
                        color = text_color,
                        text_align = 'center',
                        vertical_align = 'center',
                        interline = 1
                       ).with_position(('center', 'center'))
    return num_clip


def create_sliding_clips(text_string: str, num: str, start_time: int, font: str):
    """
    This function produces a list of text clips where a num slides across the screen in the middle of the text string.
    Requires that the text string contain 5 linebreaks in the middle.
    :param text_string: The string to display for entire clip
    :param num: The number (or numerical string) to slide across the screen
    :param start_time: Time (in seconds) to start the sequence of clips
    :param font: Filepath for font file
    :return: List of MoviePy TextClips with given contents
    """
    sliding_intro = create_text_clip(screen_size,
                                     font,
                                     75,
                                     black,
                                     text_string
                                     ).with_duration(8).with_start(start_time).with_effects(
        [vfx.CrossFadeIn(2).copy(), vfx.CrossFadeOut(1.5).copy()])

    sliding_in = create_num_clip(screen_size,
                                 font,
                                 150,
                                 white,
                                 str(num)
                                 ).with_duration(3).with_start(start_time + 1).with_effects(
        [vfx.SlideIn(1, 'left').copy()])

    sliding_out = create_num_clip(screen_size,
                                  font,
                                  150,
                                  white,
                                  str(num)
                                  ).with_duration(3).with_start(start_time + 4).with_effects(
        [vfx.SlideOut(1, 'right').copy()])
    return [sliding_intro, sliding_in, sliding_out]