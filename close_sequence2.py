
import pandas as pd
import numpy as np
import re
import xlsxwriter
import win32com.client as win32
from datetime import date, datetime
from great_tables import GT
from moviepy import *


def close(dictionary, background_color,  font_1, meme_path, duration_start):
    video_list = []

    standard_duration = 7
    start_duration = duration_start
    stop_duration_sum = duration_start
    interval = .5



    intro_text = (TextClip(
        font=font_1,
        text="What a way to finish \n the calendar year!",
        font_size=65,
        color="#000000",
        text_align="center",
        margin = (15,15))
                  .with_position(("center", "center"))
                  .with_duration(standard_duration)
                  .with_start(start_duration + interval)
                  .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                  )
    video_list.append(intro_text)

    stop_duration_sum += standard_duration+interval

    print('worst metric ' + str(dictionary['Productivity: Worst Metric']))


    productivity_dictionary = {'Visits':["visit",str(int(dictionary['Productivity: Difference to Goal']))+" visits"],
                               'Qualifications':["qualification",str(int(dictionary['Productivity: Difference to Goal']))+" qualifications"],
                               'Booked Amount':["booked amount","$" + (str(int(dictionary['Productivity: Difference to Goal']/1000))+"K" if dictionary['Productivity: Difference to Goal']<1000000 else str(round(dictionary['Productivity: Difference to Goal']/1000000,2))+"M") +" booked"],
                               'Asked ($100k+)':["$100k+ asked ",str(int(dictionary['Productivity: Difference to Goal']))+" $100K+ asks"],
                               'Booked':["booked",str(int(dictionary['Productivity: Difference to Goal']))+" booked proposals"],
                               'Asked':["asked",str(int(dictionary['Productivity: Difference to Goal']))+" asked proposals"],
                               'Asked Amount':["asked amount","$" + (str(int(dictionary['Productivity: Difference to Goal']/1000))+"K" if dictionary['Productivity: Difference to Goal']<1000000 else str(round(dictionary['Productivity: Difference to Goal']/1000000,2))+"M") + " asked"],
                               }

    # dictionary['Productivity: Difference to Goal']
    # dictionary['Productivity: Worst Metric']

    if dictionary['Productivity: Worst Metric'] != '':
        lowest_pace_goal, number_and_productivity_metric = productivity_dictionary[dictionary['Productivity: Worst Metric']]
        print(dictionary['Final Name'] + ' / beat your ' + lowest_pace_goal + " goal! / You have " + number_and_productivity_metric + " to do")

        if dictionary['Productivity: Difference to Goal'] >0:

          #  lowest_pace_goal = dictionary['Productivity: Worst Metric']
            call_to_action_text = (TextClip(
                font=font_1,
                text=f"We know \n you want to finish \n the fiscal year \n just as strong.\n\n\nWe challenge you \n to beat your \n {lowest_pace_goal} goal!",
                font_size=65,
                color="#000000",
                text_align="center",
            margin = (15,15))
                          .with_position(("center", "center"))
                          .with_duration(standard_duration)
                          .with_start(stop_duration_sum + interval)
                          .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                          )
            video_list.append(call_to_action_text)

            stop_duration_sum += standard_duration + interval

            string_1 = f"You have\n{number_and_productivity_metric}\nto do\n in the second half\n of the fiscal year.\n\n\nIf you need help\nor have any questions,\n  reach out to \nyour manager \nor\nProspect Development\nLiasons"
            string_2 = f"You are\n{number_and_productivity_metric}\naway from\nachieving your goal\n this fiscal year.\n\n\nIf you need help\nor have any questions,\n  reach out to \nyour manager \nor\nProspect Development\nLiasons."
            string_3 = f"You are{number_and_productivity_metric}away from achieving your goal in the second half of the fiscal year. If you need help or have any questions, reach out to your manager or Prospect Development Liasons."

            call_to_action_text2 = (TextClip(
                font=font_1,
                text=string_2,
                font_size=65,
                color="#000000",
                text_align="center",
            margin = (15,15))
                                   .with_position(("center", "center"))
                                   .with_duration(standard_duration)
                                   .with_start(stop_duration_sum + interval)
                                   .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                                   )
            video_list.append(call_to_action_text2)

            stop_duration_sum += standard_duration + interval

        elif dictionary['Productivity: Difference to Goal'] <0:
            call_to_action_text3 = (TextClip(
                font=font_1,
                text=f"You've \n crushed \n your goals \n for FY24! \n Keep up \n the great work!",
                font_size=65,
                color="#000000",
                text_align="center",
            margin = (15,15))
                                    .with_position(("center", "center"))
                                    .with_duration(standard_duration)
                                    .with_start(stop_duration_sum + interval)
                                    .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                                    )
            video_list.append(call_to_action_text3)

            stop_duration_sum += standard_duration + interval

    else:
        call_to_action_text = (TextClip(
            font=font_1,
            text=f"We know \n you want to finish \n the fiscal year \n just as strong.",
            font_size=65,
            color="#000000",
            text_align="center",
            margin=(15, 15))
                               .with_position(("center", "center"))
                               .with_duration(standard_duration)
                               .with_start(stop_duration_sum + interval)
                               .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                               )
        video_list.append(call_to_action_text)

        stop_duration_sum += standard_duration + interval
    meme_clip = (ImageClip(meme_path)
            .with_position(("center", "center"))
            .with_duration(standard_duration)
            .with_start(stop_duration_sum + interval)
            .with_effects([vfx.Resize(width=1000),
                           vfx.CrossFadeIn(1).copy(),
                           vfx.CrossFadeOut(1).copy()])
            )
    video_list.append(meme_clip)
    stop_duration_sum += standard_duration + interval

    gift_officer_name = dictionary['Final Name']

    final_text = (TextClip(
            font=font_1,
            text=f"\n {gift_officer_name},\nthank you\n for a great\n 2024!\n\n\n\n\n\n\n\n\n ",
            font_size=70,
            color="#000000",
            text_align="center",
        margin = (15,15))
                               .with_position(("center", "center"))
                               .with_duration(standard_duration)
                               .with_start(stop_duration_sum + interval)
                               .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                               )
    video_list.append(final_text)

    final_text2 = (TextClip(
        font=font_1,
        text=f"\n\n\n\n\n\n\n\n\n\n\n ARD Year in Review\nis brought to you \n by \n Prospect Development \n & Decision Support Team \n",
        font_size=40,
        color="#000000",
        text_align="center",
        margin = (15,15))
                  .with_position(("center", "center"))
                  .with_duration(standard_duration)
                  .with_start(stop_duration_sum + interval)
                  .with_effects([vfx.CrossFadeIn(1).copy(), vfx.CrossFadeOut(1).copy()])
                  )
    video_list.append(final_text2)

    stop_duration_sum += standard_duration + interval

    stop_duration_sum += 4
    total_duration = stop_duration_sum - start_duration

    background_clip = (ColorClip(size=(1080,1920),
                                 color=background_color)
                       .with_fps(30)
                       .with_start(start_duration).with_duration(total_duration)
                       .with_effects([vfx.CrossFadeIn(1.5).copy(), vfx.CrossFadeOut(2).copy()])
                       )

    video_list.insert(0,background_clip)


    return video_list, stop_duration_sum

