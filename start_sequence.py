
import pandas as pd
import numpy as np
import re
import xlsxwriter
import win32com.client as win32
from datetime import date, datetime
from great_tables import GT
from moviepy import *


def start_series(dictionary, background_color, font_1, font_2, meme_path, username):
    video_list = []
    duration = 0
    gift_officer_name = dictionary['Final Name']
    interval = 1

    phoenix_path = fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\UChicago_Phoenix_Outlined_1Color_White_RGB.png"

    phoenix = (ImageClip(phoenix_path)
            .with_position(("center", "center"))
            .with_duration(7)
            .with_start(1)
            .with_effects([#vfx.Resize(width=1080),
                           vfx.CrossFadeIn(1).copy(),
                           vfx.CrossFadeOut(1).copy()])
            )
    video_list.append(phoenix)

    text1 = "Thanks \n to all of \n your great work, \n \nARD \nhad a spectacular \n2024!"
    text2 = "University\nof Chicago's\nARD\nhad a\nspectacular\n2024!"

    intro_text = (TextClip(
        font=font_1,
        text=text2,
        font_size=100,
        color="#000000",
        text_align="center",
        margin = (15,15))
                  .with_position(("center", "center"))
                  .with_duration(7)
                  .with_start(1)
                  .with_effects([vfx.CrossFadeIn(1).copy(),
                                 vfx.CrossFadeOut(1).copy()])
                  )
    video_list.append(intro_text)
    duration += 7 + interval

    meme = (ImageClip(meme_path)
            .with_position(("center", "center"))
            .with_duration(5)
            .with_start(duration)
            .with_effects([vfx.Resize(width=1000).copy(),
                           vfx.CrossFadeIn(1).copy(),
                           vfx.CrossFadeOut(1).copy()])
            )
    video_list.append(meme)

    duration += 5 + interval

    thanks_text = (TextClip(
        font=font_1,
        text="As a special \nthank you, \n\n we wanted to \n celebrate all that "
             "\nYOU \naccomplished \nin 2024 \n\n(and have \na little fun \nalong the way…)",
        font_size=65,
        color="#000000",
        text_align="center",
        margin = (15,15)
    ).with_position(("center", "center"))
    .with_duration(7)
    .with_start(duration-1)
    .with_effects([vfx.CrossFadeIn(1).copy(),
                   vfx.CrossFadeOut(1).copy()]))

    duration += 7 + interval-2
    video_list.append(thanks_text)

    close_text_intro = f"Introducing\n{gift_officer_name}'s\n2024\nFundraising\nYear in Review!\n"

    close_text = (TextClip(
        font=font_1,
        text=close_text_intro,
        font_size=75,
        color="#000000",
        text_align="center",
        vertical_align = 'center',
        #bg_color = (255,255,255),
        margin = (15,15)
    ).with_position(("center", "center"))
                  .with_duration(7)
                  .with_start(duration)
                  .with_effects([vfx.CrossFadeIn(1).copy(),
                                 vfx.CrossFadeOut(1).copy()]))
    video_list.append(close_text)
    duration += 7 + interval

    background_clip = (ColorClip(size=(1080, 1920),
                                 color=background_color)
                       .with_fps(30)
                       .with_duration(duration)
                       .with_start(0)
                       .with_effects([vfx.CrossFadeIn(1.5).copy(),
                                      vfx.CrossFadeOut(1).copy()]))
    video_list.insert(0, background_clip)

    return video_list, duration
