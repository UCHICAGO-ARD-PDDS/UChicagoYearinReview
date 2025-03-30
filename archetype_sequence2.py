import random

import pandas as pd
import numpy as np
import re
import xlsxwriter
import win32com.client as win32
from datetime import date, datetime
from great_tables import GT
from moviepy import *

class Archetype:


    def __init__(self, dictionary, background_color, duration, font_1, meme_path, username):
        self.path = fr'C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\archetype_images2'
        self.images = [r'\1st layer.png',
                  r'\2nd layer.png',
                  r'\3rd layer.png',
                  r'\4th layer.png',
                  r'\5th layer.png']
        self.locator = self.path + r'\Locator.png'
        self.question = self.path + r'\Question.png'

        self.video_list = []
        self.duration = duration

        standard_duration = 6
        start_duration = duration
        self.stop_duration_sum = duration
        interval = 1

        intro_text = (TextClip(
            font=font_1,
            text="(Almost) everyone knows \n about the Myers Briggs \n personality test…",
            font_size=65,
            color="#000000",
            text_align="center",
        margin = (15,15))
                      .with_position(("center", "center"))
                      .with_duration(standard_duration)
                      .with_start(start_duration + interval + 1)
                      .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                      )
        self.video_list.append(intro_text)

        self.stop_duration_sum += standard_duration + interval + 1

        meme_clip = (ImageClip(meme_path)
                     .with_position(("center", "center"))
                     .with_duration(standard_duration)
                     .with_start(self.stop_duration_sum + interval)
                     .with_effects([vfx.Resize(width=1000),
                                    vfx.CrossFadeIn(1).copy(),
                                    vfx.CrossFadeOut(1).copy()])
                     )
        self.video_list.append(meme_clip)

        self.stop_duration_sum += standard_duration + interval

        long_text_contents = """But only ARD has the Afsahi-
        Malmquist fundraiser type 
        test to describe your 
        fundraising style. 
    
    It's based on your real results 
    from 2024 and we're 
    confident you'll maybe, 
    probably learn something 
    about yourself. 
    
    Just like Myers Briggs - we 
    know you may have some thoughts;  
    please email: 
    armin@uchicago.edu 
    to share any feedback."""

        long_text_contents2 = (
 """But only ARD has the 
Afsahi-Malmquist
Fundraiser Type 
test to describe your 
fundraising style.
         
         
It's based on your real results 
from 2024 and we're
confident you'll maybe,
 probably learn something
about yourself."""
                               )

        long_text = (TextClip(
            font=font_1,
            text=long_text_contents2,
            font_size=65,
            color="#000000",
            text_align="center",
        margin = (15,15))
                      .with_position(("center", "center"))
                      .with_duration(standard_duration)
                      .with_start(self.stop_duration_sum + interval)
                      .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                      )
        self.video_list.append(long_text)
        self.stop_duration_sum += standard_duration + interval


        # Set acronym and variables for archetype graphics
        acronym = ''

        if dictionary['Visits: Count'] > 0:
            visit_ratio = dictionary['Visits: Virtual Visits'] / dictionary['Visits: Count']
            if visit_ratio >= .5:
                acronym += 'D'
            else:
                acronym += 'I'
            visit_skip = True
        else:
            visit_ratio = 0.5
            visit_skip = False

        if dictionary["Asks: Count"]>0:
            ask_ratio = dictionary["Asks: Count No Shared Credit"]/dictionary["Asks: Count"]
            print(dictionary["Asks: Count No Shared Credit"])
            print(dictionary["Asks: Count"])
            print('Ask Ratio:')
            print(ask_ratio)

            if ask_ratio >= .5:
                acronym += 'P'
            else:
                acronym += 'S'
            ask_skip = True
        else:
            ask_skip = False
            ask_ratio = 0.5

        if dictionary['Managers: Percentile']:
            managers_ratio = dictionary['Managers: Percentile']

            if managers_ratio >= .5:
                acronym += 'G'
            else:
                acronym += 'T'
            managers_skip = True
        else:
            managers_skip = False
            managers_ratio = 0.5

        if dictionary['Time at ARD: Percentile']:

            time_ratio = dictionary['Time at ARD: Percentile']

            if time_ratio >= .5:
                acronym += 'V'
            else:
                acronym += 'N'
            time_skip = True
        else:
            time_skip = False
            time_ratio = 0.5

        if dictionary["Qualifications: Count"]>0:
            qual_ratio = dictionary["Qualifications: Prospects Qualified for Multiple Units"]/dictionary["Qualifications: Count"]
            print(dictionary["Qualifications: Prospects Qualified for Multiple Units"])
            print(dictionary["Qualifications: Count"])
            print('Qual Ratio:')
            print(qual_ratio)

            if qual_ratio >= .5:
                acronym += 'M'
            else:
                acronym += 'E'

            qual_skip = True
        else:
            qual_skip = False
            qual_ratio = 0.5

        # New text
        new_text_contents = f"""
It certainly sounds
cooler than INTJ
or ENTP.

Let us tell you 
what it means:
        """

        celebaration_text = f"You are a {acronym}!"

        new_text_contents_2= f"""
You are a {acronym}!

It certainly sounds
cooler than INTJ
or ENTP.

Let us tell you 
what it means:
        """

        new_text = (TextClip(
            font=font_1,
            text=new_text_contents_2,
            #text="You are a champion!",
            font_size=65,
            color="#000000",
            text_align="center",
        margin = (15,15))
                    .with_position(("center", "center"))
                    .with_duration(standard_duration)
                    .with_start(self.stop_duration_sum + interval)
                    .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                    )
        self.video_list.append(new_text)

        new_text_2 = (TextClip(
            font=font_1,
            text=new_text_contents,
            font_size=65,
            color="#000000",
            text_align="center",
        margin = (15,15))
                    .with_position((.22,0.45), relative=True)
                    .with_duration(standard_duration)
                    .with_start(self.stop_duration_sum + interval)
                    .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                    )
        # self.video_list.append(new_text_2)

        self.stop_duration_sum += standard_duration + interval

       # Graphic's
        graphic_interval = 3
        buffer = 1.5

        self.archetype_graphic(1,
                               self.stop_duration_sum,
                               graphic_interval,
                               439,
                               363,
                               buffer,
                               (visit_ratio*410)+270,
                               visit_skip)



        self.archetype_graphic(2,
                               self.stop_duration_sum,
                               graphic_interval,
                               439,
                               679,
                               buffer,
                               (ask_ratio*410)+270,
                               ask_skip)



        self.archetype_graphic(3,
                               self.stop_duration_sum,
                               graphic_interval,
                               439,
                               993,
                               buffer,
                               (managers_ratio*410)+270,
                               managers_skip)



        self.archetype_graphic(4,
                               self.stop_duration_sum,
                               graphic_interval,
                               439,
                               1313,
                               buffer,
                               (time_ratio*410)+270,
                               time_skip)


        self.archetype_graphic(5,
                               self.stop_duration_sum,
                               graphic_interval,
                               439,
                               1632,
                               buffer,
                               (qual_ratio*410)+270,
                               qual_skip)

        self.stop_duration_sum += (graphic_interval*5)+(buffer*2)+ interval+4

        closing_text1 = """
Let us know,
do you think your
Afsahi-Malmquist
Fundraiser type 
is accurate?
"""

        closing_text2 = f"""
What would you 
call a {acronym} 
Fundraiser? 

Are you an innovator, 
relationship master, 
bridge builder?
Something else? 
"""

        closing_test_list = [closing_text1, closing_text2]
        random_text = random.sample(closing_test_list, 1)[0]

        closing_text = (TextClip(
            font=font_1,
            text=random_text,
            font_size=65,
            color="#000000",
            text_align="center",
        margin = (15,15))
                     .with_position(("center", "center"))
                     .with_duration(standard_duration-1)
                     .with_start(self.stop_duration_sum+6)
                     .with_effects([vfx.CrossFadeIn(1).copy(),
                                    vfx.CrossFadeOut(1).copy()])
                     )
        self.video_list.append(closing_text)
        self.stop_duration_sum += standard_duration + interval

        self.stop_duration_sum += 5.5
        total_duration = self.stop_duration_sum - start_duration

        background_clip = (ColorClip(size=(1080, 1920),
                                     color=background_color)
                           .with_fps(30)
                           .with_start(start_duration).with_duration(total_duration)
                           .with_effects([vfx.CrossFadeIn(1.5).copy(),
                                          vfx.CrossFadeOut(2).copy()])
                           )

        self.video_list.insert(0, background_clip)


    def archetype_graphic(self, ag_interval, start, interval, x, y,buffer,x2, dont_skip):

        image_path = self.path + self.images[ag_interval-1]

        graphic = (ImageClip(image_path)
                     .with_position(("center", "center"))
                     .with_duration((interval*(5-(ag_interval-1)+(buffer*2)))+4)
                     .with_start(start+(interval*(ag_interval-1))+buffer)
                     .with_effects([vfx.CrossFadeIn(1).copy(),
                                    vfx.CrossFadeOut(1).copy()])
                     )
        self.video_list.append(graphic)

        if dont_skip:
            graphic2 = (ImageClip(self.locator)
                       .with_position((x2,y-25))
                        .with_duration((interval * (5 - (ag_interval - 1) + (buffer * 2)))+4)
                        .with_start(start + (interval * (ag_interval - 1)) + buffer)
                       .with_effects([vfx.CrossFadeIn(1).copy(),
                                      vfx.CrossFadeOut(1).copy()])
                       )
            self.video_list.append(graphic2)

        elif ~dont_skip:
            graphic2 = (ImageClip(self.question)
                        .with_position((x2, y - 25))
                        .with_duration((interval * (5 - (ag_interval - 1) + (buffer * 2))) + 4)
                        .with_start(start + (interval * (ag_interval - 1)) + buffer)
                        .with_effects([vfx.CrossFadeIn(1).copy(),
                                       vfx.CrossFadeOut(1).copy()])
                        )
            self.video_list.append(graphic2)

