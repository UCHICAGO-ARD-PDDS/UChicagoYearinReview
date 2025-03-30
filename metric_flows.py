from metric_clips import *
from matplotlib import font_manager
import textwrap
import matplotlib.pyplot as plt
import pandas as pd
from moviepy import *
from pathlib import Path

percentile_slide_threshold = 0.6
amount_slide_threshold = 4999

clip_fps = 30

black = (0, 0, 0)
white = (255, 255, 255)

### Check campus visit ###
### Write image files somewhere new ###


def plan_contacts(go_row: dict, percentile_threshold: float):
    """
    This function takes in a GO dict and determines the duration of the contacts clip sequence.
    The minimum length is 24 seconds, but the sequence can get up to 40 seconds
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param percentile_threshold: Threshold used to determine if percentile is included
    :return: Full duration of sequence, Boolean for percentile slide, Boolean for booked slide
    """
    full_duration = 24
    sec_per_clip = 8

    percentile_trigger = False
    if go_row['Contacts: Percentile'] >= percentile_threshold:
        percentile_trigger = True
        full_duration += sec_per_clip

    booked_trigger = False
    if go_row['Contacts: Most Contacted Household Booked?']:
        booked_trigger = True
        full_duration += sec_per_clip

    return full_duration, percentile_trigger, booked_trigger


def write_contacts_clip(go_row: dict, bg_color: tuple, font: str, start_time: int, clip_duration: int,
                        percentile_trigger: bool, booked_trigger: bool, photos: list):
    """
    This function takes in a GO dict and returns a list of all contacts clips.

    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param font: Filepath for font file
    :param bg_color: The color to use for the background
    :param start_time: Starting time (in seconds) for sequence
    :param clip_duration: Total duration of sequence
    :param percentile_trigger: Trigger for percentile slide
    :param booked_trigger: Trigger for booked slide
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for contacts sequence, Duration of full sequence
    """
    contacts_clips_list = []
    running_duration = 0

    contacts_bg_clip = create_background_clip(clip_size=screen_size,
                                              bg_color=bg_color,
                                              fps=clip_fps).with_duration(clip_duration).with_start(start_time).with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    contacts_clips_list.append(contacts_bg_clip)

    #contacts_clips_list.extend(all_scrapbook_clips(clip_duration, photos))

    contacts_intro_clip = create_text_clip(screen_size,
                                           font,
                                           75,
                                           black,
                                           "We know the heart of\nbuilding relationships\nwith our prospects is\ncommunicating with them."
                                           ).with_duration(8).with_start(start_time).with_end(start_time+8).with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    contacts_clips_list.append(contacts_intro_clip)
    running_duration += 8

    contacts_clips_list.extend(
        create_sliding_clips("In 2024,\nyou made\n\n\n\n\ncontacts!\n ", str(int(go_row['Contacts: Count'])),
                             start_time+running_duration, font))
    running_duration += 8

    if percentile_trigger:
        get_ordinal = lambda n: str(n) + 'tsnrhtdd'[n % 5 * (n % 100 ^ 15 > 4 > n % 10)::4]
        cleaned_percentile = get_ordinal(int(round(go_row['Contacts: Percentile'] * 100, 0)))
        contacts_clips_list.extend(
            create_sliding_clips("This places\nyou in the\n\n\n\n\npercentile\nat ARD.", str(cleaned_percentile),
                                 start_time+running_duration, font))
        running_duration += 8

    contacts_clips_list.extend(create_sliding_clips("You contacted\none household\n\n\n\n\ntimes.\n ",
                                                    str(int(go_row['Contacts: Most Contacts for Household'])),
                                                    start_time+running_duration, font))
    running_duration += 8

    if booked_trigger:
        contacts_booked = create_text_clip(screen_size,
                                           font,
                                           75,
                                           black,
                                           "And they made a\ndonation!"
                                           ).with_duration(8).with_start(start_time+running_duration).with_effects(
            [vfx.CrossFadeIn(2).copy(), vfx.CrossFadeOut(1.5).copy()])
        contacts_clips_list.append(contacts_booked)
        running_duration += 8

    print(running_duration == clip_duration)

    return contacts_clips_list, start_time + running_duration


def run_contacts(go_row: dict, bg_color: tuple, start_time: int, font: str, photos: list):
    """
    This function takes in a GO dictionary, determines the slides to use in the contacts sequence,
    and creates the list of clips to return
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param start_time: Start time (in seconds) of contacts sequence
    :param font: Filepath for font file
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for contacts sequence, Duration of full sequence
    """
    contacts_duration, percentile_slide, booked_slide = plan_contacts(go_row, percentile_slide_threshold)
    return write_contacts_clip(go_row, bg_color, font, start_time, contacts_duration, percentile_slide, booked_slide, photos)





def plan_visits(go_row: dict, percentile_threshold: float):
    """
    This function takes in a GO dict and determines the duration of the visits clip sequence.
    The minimum length is 24 seconds, but the sequence can get up to 32 seconds
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param percentile_threshold: Threshold used to determine if percentile is included
    :return: Full duration of sequence, Boolean for percentile slide
    """
    full_duration = 16
    sec_per_clip = 8

    percentile_trigger = False
    if go_row['Visits: Percentile'] >= percentile_threshold:
        percentile_trigger = True
        full_duration += sec_per_clip

    campus_trigger = False
    if go_row['Visits: Campus Visits'] > 1:
        campus_trigger = True
        full_duration += sec_per_clip

    return full_duration, percentile_trigger, campus_trigger


def write_visits_clip(go_row: dict, bg_color: tuple, font: str, start_time: int, clip_duration: int,
                      percentile_trigger: bool, campus_trigger: bool, photos: list):
    """
    This function takes in a GO dict and returns a list of all visits clips.

    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param font: Filepath for font file
    :param start_time: Starting time (in seconds) for sequence
    :param clip_duration: Total duration of sequence
    :param percentile_trigger: Trigger for percentile slide
    :param campus_trigger: Trigger for campus visits slide
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for visits sequence, Duration of full sequence
    """
    visits_clips_list = []
    running_duration = 0

    visits_bg_clip = create_background_clip(clip_size=screen_size,
                                            bg_color=bg_color,
                                            fps=clip_fps).with_duration(clip_duration).with_start(start_time).with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    visits_clips_list.append(visits_bg_clip)

    #visits_clips_list.extend(all_scrapbook_clips(clip_duration, photos))

    visits_intro_clip = create_text_clip(screen_size,
                                         font,
                                         75,
                                         black,
                                         "Visiting with\nprospects is vital to\ndeepening their\nrelationship with\nthe University."
                                         ).with_duration(8).with_start(start_time).with_end(start_time+8).with_effects(
        [vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    visits_clips_list.append(visits_intro_clip)
    running_duration += 8

    visits_clips_list.extend(
        create_sliding_clips("In 2024,\nyou participated in\n\n\n\n\nvisits!\n ", str(int(go_row['Visits: Count'])),
                             start_time+running_duration, font))
    running_duration += 8

    if percentile_trigger:
        get_ordinal = lambda n: str(n) + 'tsnrhtdd'[n % 5 * (n % 100 ^ 15 > 4 > n % 10)::4]
        cleaned_percentile = get_ordinal(int(round(go_row['Visits: Percentile'] * 100, 0)))
        visits_clips_list.extend(
            create_sliding_clips("This places\nyou in the\n\n\n\n\npercentile\nat ARD.", str(cleaned_percentile),
                                 start_time+running_duration, font))
        running_duration += 8

    if campus_trigger:
        visits_clips_list.extend(
            create_sliding_clips("Through those visits,\n you brought\n\n\n\n\nhouseholds to our\nawesome campus!",
                                 str(int(go_row['Visits: Campus Visits'])), start_time+running_duration, font))
        running_duration += 8

    print(running_duration == clip_duration)

    return visits_clips_list, running_duration + start_time


def run_visits(go_row: dict, bg_color: tuple, start_time: int, font: str, photos: list):
    """
    This function takes in a GO dictionary, determines the slides to use in the visits sequence,
    and creates the list of clips to return
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param start_time: Start time (in seconds) of visits sequence
    :param font: Filepath for font file
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for visits sequence, Duration of full sequence
    """
    visits_duration, percentile_slide, campus_slide = plan_visits(go_row, percentile_slide_threshold)
    return write_visits_clip(go_row, bg_color, font, start_time, visits_duration, percentile_slide, campus_slide, photos)





def plan_qualifications(go_row: dict, percentile_threshold: float, amount_threshold: int):
    """
    This function takes in a GO dict and determines the duration of the qualifications clip sequence.
    The minimum length is 24 seconds, but the sequence can get up to 40 seconds
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param percentile_threshold: Threshold used to determine if percentile is included
    :param amount_threshold: Threshold used to determine if the amount qualified is included
    :return: Full duration of sequence, Boolean for percentile slide
    """
    full_duration = 24
    sec_per_clip = 8

    percentile_trigger = False
    if go_row['Qualifications: Percentile'] >= percentile_threshold:
        percentile_trigger = True
        full_duration += sec_per_clip

    amount_trigger = False
    if go_row['Qualifications: Amount for Most Qualified Unit'] >= amount_threshold:
        amount_trigger = True
        full_duration += sec_per_clip

    return full_duration, percentile_trigger, amount_trigger


def write_qualifications_clip(go_row: dict, bg_color: tuple, font: str, start_time: int, clip_duration: int,
                              percentile_trigger: bool, amount_trigger: bool, photos: list):
    """
    This function takes in a GO dict and returns a list of all qualifications clips.

    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param font: Filepath for font file
    :param start_time: Starting time (in seconds) for sequence
    :param clip_duration: Total duration of sequence
    :param percentile_trigger: Trigger for percentile slide
    :param amount_trigger: Trigger for amount slide
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for qualifications sequence, Duration of full sequence
    """
    qualifications_clips_list = []
    running_duration = 0

    qualifications_bg_clip = create_background_clip(clip_size=screen_size,
                                                    bg_color=bg_color,
                                                    fps=clip_fps).with_duration(clip_duration).with_start(start_time).with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    qualifications_clips_list.append(qualifications_bg_clip)

    #qualifications_clips_list.extend(all_scrapbook_clips(clip_duration, photos))

    qualifications_intro_clip = create_text_clip(screen_size,
                                                 font,
                                                 75,
                                                 black,
                                                 "The better we\nknow our prospects,\nthe better we\ncan build a\ncompelling proposal."
                                                 ).with_duration(8).with_start(start_time).with_end(start_time+8).with_effects(
        [vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    qualifications_clips_list.append(qualifications_intro_clip)
    running_duration += 8

    qualifications_clips_list.extend(create_sliding_clips("In 2024,\nyou qualified\n\n\n\n\nhouseholds!\n ",
                                                          str(int(go_row['Qualifications: Count'])), start_time+running_duration, font))
    running_duration += 8

    if percentile_trigger:
        get_ordinal = lambda n: str(n) + 'tsnrhtdd'[n % 5 * (n % 100 ^ 15 > 4 > n % 10)::4]
        cleaned_percentile = get_ordinal(int(round(go_row['Qualifications: Percentile'] * 100, 0)))
        qualifications_clips_list.extend(
            create_sliding_clips("This places\nyou in the\n\n\n\n\npercentile\nat ARD.", str(cleaned_percentile),
                                 start_time+running_duration, font))
        running_duration += 8

    qualifications_clips_list.extend(create_sliding_clips(
        f"Of those qualifications,\n you qualified\n\n\n\n\nstrategies for\n{go_row['Qualifications: Most Qualified Unit']}.",
        str(int(go_row['Qualifications: Count for Most Qualified Unit'])), start_time+running_duration, font))
    running_duration += 8

    if amount_trigger:
        cleaned_amount = human_format(int(go_row['Qualifications: Amount for Most Qualified Unit']))
        qualifications_amount = create_text_clip(screen_size,
                                                 font,
                                                 75,
                                                 black,
                                                 f"With a total\nqualification\namount of \n{cleaned_amount}!"
                                                 ).with_duration(8).with_start(start_time+running_duration).with_effects(
            [vfx.CrossFadeIn(2).copy(), vfx.CrossFadeOut(1.5).copy()])
        qualifications_clips_list.append(qualifications_amount)
        running_duration += 8

    print(running_duration == clip_duration)

    return qualifications_clips_list, running_duration + start_time

def run_qualifications(go_row: dict, bg_color: tuple, start_time: int, font: str, photos: list):
    """
    This function takes in a GO dictionary, determines the slides to use in the qualifications sequence,
    and creates the list of clips to return
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param start_time: Start time (in seconds) of qualifications sequence
    :param font: Filepath for font file
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for qualifications sequence, Duration of full sequence
    """
    quals_duration, percentile_slide, amount_slide = plan_qualifications(go_row, percentile_slide_threshold, amount_slide_threshold)
    return write_qualifications_clip(go_row, bg_color, font, start_time, quals_duration, percentile_slide, amount_slide, photos)





def plan_asks(go_row: dict, percentile_threshold: float):
    """
    This function takes in a GO dict and determines the duration of the asks clip sequence.
    The minimum length is 24 seconds, but the sequence can get up to 40 seconds
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param percentile_threshold: Threshold used to determine if percentile is included
    :return: Full duration of sequence, Boolean for percentile slide, Boolean for booked slide
    """
    full_duration = 24
    sec_per_clip = 8

    percentile_trigger = False
    if go_row['Asks: Percentile'] >= percentile_threshold:
        percentile_trigger = True
        full_duration += sec_per_clip

    booked_trigger = False
    if go_row['Asks: Largest Ask Booked?']:
        booked_trigger = True
        full_duration += sec_per_clip

    return full_duration, percentile_trigger, booked_trigger


def write_asks_clips(go_row: dict, bg_color: tuple, font: str, start_time: int, clip_duration: int,
                     percentile_trigger: bool, booked_trigger: bool, photos: list):
    """
    This function takes in a GO dict and returns a list of all asks clips.

    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param font: Filepath for font file
    :param start_time: Starting time (in seconds) for sequence
    :param clip_duration: Total duration of sequence
    :param percentile_trigger: Trigger for percentile slide
    :param booked_trigger: Trigger for booked slide
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for asks sequence, Duration of full sequence
    """
    asks_clips_list = []
    running_duration = 0

    asks_bg_clip = create_background_clip(clip_size=screen_size,
                                          bg_color=bg_color,
                                          fps=clip_fps).with_duration(clip_duration).with_start(start_time).with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    asks_clips_list.append(asks_bg_clip)

   # asks_clips_list.extend(
    #    all_scrapbook_clips(clip_duration, photos))

    asks_intro_clip = create_text_clip(screen_size,
                                       font,
                                       75,
                                       black,
                                       "Asking prospects to\nsupport the University\nmay be the most\nimportant work we do."
                                       ).with_duration(8).with_start(start_time).with_end(start_time+8).with_effects(
        [vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    asks_clips_list.append(asks_intro_clip)
    running_duration += 8

    asks_clips_list.extend(
        create_sliding_clips("In 2024,\nyou asked\n\n\n\n\nproposals!\n ", str(int(go_row['Asks: Count'])),
                             start_time+running_duration, font))
    running_duration += 8

    if percentile_trigger:
        get_ordinal = lambda n: str(n) + 'tsnrhtdd'[n % 5 * (n % 100 ^ 15 > 4 > n % 10)::4]
        cleaned_percentile = get_ordinal(int(round(go_row['Asks: Percentile'] * 100, 0)))
        asks_clips_list.extend(
            create_sliding_clips("This places\nyou in the\n\n\n\n\npercentile for asked\namount at ARD.", str(cleaned_percentile),
                                 start_time+running_duration, font))
        running_duration += 8

    cleaned_amount = human_format(int(go_row['Asks: Largest Ask']))
    asks_clips_list.extend(
        create_sliding_clips("Your largest asked\nproposal was for\n\n\n\n\n", str(cleaned_amount), start_time+running_duration, font))
    running_duration += 8

    if booked_trigger:
        asks_booked = create_text_clip(screen_size,
                                       font,
                                       75,
                                       black,
                                       "And you booked it!"
                                       ).with_duration(8).with_start(start_time+running_duration).with_effects(
            [vfx.CrossFadeIn(2).copy(), vfx.CrossFadeOut(1.5).copy()])
        asks_clips_list.append(asks_booked)
        running_duration += 8

    print(running_duration == clip_duration)

    return asks_clips_list, running_duration + start_time


def run_asks(go_row: dict, bg_color: tuple, start_time: int, font: str, photos: list):
    """
    This function takes in a GO dictionary, determines the slides to use in the asks sequence,
    and creates the list of clips to return
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param start_time: Start time (in seconds) of asks sequence
    :param font: Filepath for font file
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for asks sequence, Duration of full sequence
    """
    ask_duration, percentile_slide, booked_slide = plan_asks(go_row, percentile_slide_threshold)
    return write_asks_clips(go_row, bg_color, font, start_time, ask_duration, percentile_slide, booked_slide, photos)



graph_colors = [(234, 170, 0), (222, 124, 0), (120, 157, 74), (39, 93, 56), (0, 115, 150), (89, 49, 95), (164, 52, 58)]

def make_pie_chart(go_row: dict, font: str):
    """
    This function takes in a GO dictionary and a background color and creates a png image of a pie chart for their most booked units.
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param font: Filepath for font file
    :return: Filepath of newly created pie chart image
    """
    fontpath = Path(font)
    chart_font = font_manager.FontProperties(fname=fontpath)

    fig = plt.figure(figsize=(10, 7.5))
    ax = fig.add_subplot()

    units = []
    amounts = []
    for i in range(1, 5):
        units.append(go_row[f'Booked: Unit {i} Name'])
        amounts.append(go_row[f'Booked: Unit {i} Amount'])
    cleaned_units = [textwrap.fill(unit, 16) for unit in units if not pd.isnull(unit)]
    cleaned_amounts = [amount for amount in amounts if not pd.isnull(amount)]
    print(cleaned_units, cleaned_amounts)
    amount_labels = lambda pct: human_format(int(round(pct*sum(cleaned_amounts)/100.0)))

    chart_colors = random.sample(graph_colors, len(cleaned_units))
    ax.pie(cleaned_amounts, labels=cleaned_units, textprops={'fontproperties': chart_font, 'fontsize': 24},
           radius=0.9, labeldistance=1.15, startangle=225, autopct=amount_labels,
           colors=[(color[0] / 255, color[1] / 255, color[2] / 255) for color in chart_colors],
           shadow=True)
    fig.tight_layout(pad=1.5)
    filename = f"Booked Pie.png"
    fig.savefig(filename, transparent=True)
    return filename





def plan_booked(go_row: dict, percentile_threshold: float):
    """
    This function takes in a GO dict and determines the duration of the booked clip sequence.
    The minimum length is 24 seconds, but the sequence can get up to 32 seconds
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param percentile_threshold: Threshold used to determine if percentile is included
    :return: Full duration of sequence, Boolean for percentile slide
    """
    full_duration = 24
    sec_per_clip = 8

    percentile_trigger = False
    if go_row['Booked: Percentile'] >= percentile_threshold:
        percentile_trigger = True
        full_duration += sec_per_clip

    return full_duration, percentile_trigger


def write_booked_clips(go_row: dict, bg_color: tuple, font: str, start_time: int,
                       clip_duration: int, percentile_trigger: bool, photos: list):
    """
    This function takes in a GO dict and returns a list of all booked clips.

    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param font: Filepath for font file
    :param start_time: Starting time (in seconds) for sequence
    :param clip_duration: Total duration of sequence
    :param percentile_trigger: Trigger for percentile slide
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for booked sequence, Duration of full sequence
    """
    booked_clips_list = []
    running_duration = 0

    booked_bg_clip = create_background_clip(clip_size=screen_size,
                                            bg_color=bg_color,
                                            fps=clip_fps).with_duration(clip_duration).with_start(start_time).with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    booked_clips_list.append(booked_bg_clip)

   # booked_clips_list.extend(
   #     all_scrapbook_clips(clip_duration - 6, photos))

    booked_intro_clip = create_text_clip(screen_size,
                                         font,
                                         75,
                                         black,
                                         "We know this is the\nmetric everyone wants to\ntalk about..."
                                         ).with_duration(8).with_start(start_time).with_end(start_time+8).with_effects(
        [vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1.5).copy()])
    booked_clips_list.append(booked_intro_clip)
    running_duration += 8

    booked_clips_list.extend(
        create_sliding_clips("In 2024,\nyou booked\n\n\n\n\ngifts!\n ", str(int(go_row['Booked: Count'])),
                             start_time+running_duration, font))
    running_duration += 8

    if percentile_trigger:
        get_ordinal = lambda n: str(n) + 'tsnrhtdd'[n % 5 * (n % 100 ^ 15 > 4 > n % 10)::4]
        cleaned_percentile = get_ordinal(int(round(go_row['Booked: Percentile'] * 100, 0)))
        booked_clips_list.extend(
            create_sliding_clips("This places\nyou in the\n\n\n\n\npercentile for booked\namount at ARD.", str(cleaned_percentile),
                                 start_time+running_duration, font))
        running_duration += 8

    pie_chart_intro = create_text_clip(screen_size,
                                       font,
                                       75,
                                       black,
                                       "But more important\nthan the dollar amount,\nyour proposals supported\nthe following programs!\n\n\n\n\n\n\n"
                                       ).with_duration(8).with_start(start_time+running_duration).with_effects(
        [vfx.CrossFadeIn(2).copy(), vfx.CrossFadeOut(1.5).copy()])
    booked_clips_list.append(pie_chart_intro)

    pie_file_path = make_pie_chart(go_row, font)
    pie_clip = (ImageClip(pie_file_path).with_duration(8).with_start(start_time+running_duration)
                .with_position(('center', 'bottom')).with_effects(
        [vfx.CrossFadeIn(2).copy(), vfx.CrossFadeOut(1.5).copy(), vfx.Margin(bottom=350, opacity=0)]))
    booked_clips_list.append(pie_clip)
    running_duration += 8

    print(running_duration == clip_duration)

    return booked_clips_list, running_duration + start_time

def run_booked(go_row: dict, bg_color: tuple, start_time: int, font: str, photos: list):
    """
    This function takes in a GO dictionary, determines the slides to use in the booked sequence,
    and creates the list of clips to return
    :param go_row: Single row in Wrapped dataframe in dictionary form
    :param bg_color: The color to use for the background
    :param start_time: Start time (in seconds) of booked sequence
    :param font: Filepath for font file
    :param photos: List of photo filepaths for scrapbook
    :return: List of clips for booked sequence, Duration of full sequence
    """
    booked_duration, percentile_slide = plan_booked(go_row, percentile_slide_threshold)
    return write_booked_clips(go_row, bg_color, font, start_time, booked_duration, percentile_slide, photos)
