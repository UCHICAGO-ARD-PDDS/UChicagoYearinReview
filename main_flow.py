username = 'jpitfield'
# username = 'jleslie99'


import logging
scriptname = 'Wrapped 2024'
logging.basicConfig(filename=fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\wrapped_log.log",
                    level=logging.INFO,
                    format=f'%(asctime)s - {username} - %(levelname)s - %(message)s')

logging.info('Start')

import os
import pandas as pd
import numpy as np
import re
import xlsxwriter
import win32com.client as win32
from datetime import date, datetime
from great_tables import GT
from moviepy import *
from start_sequence import start_series
from archetype_sequence2 import Archetype
from close_sequence2 import close
from metric_clips import *
from metric_flows import *
import random
# from pyfonts import load_font

df_go_metrics = pd.read_csv(fr'C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\Wrapped 24 Data.csv', low_memory=False)
df_go_metrics = pd.read_csv(fr'C:\Users\{username}\Downloads\Qualification Correction.csv')

gotham_medium_font = r"C:\Windows\Fonts\Gotham-Medium.otf"
garamond_regular = r"C:\Windows\Fonts\GARABD.ttf"

uchicago_background_colors = [(243,208,62), # light Goldenrod
                              (236,161,84), # light terracotta
                              (169,196,127), #light ivy
                              (156, 175, 136),  # light forest
                              (62, 177, 200),  # light lake
                              (134, 100, 122),  # light violet
                              (180, 106, 85),  # light brick
]

def get_file_paths(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths
# import UChicago fonts


list_of_music = get_file_paths(music_folder_path)

list_of_videos = ['','','','','',
                 '','','','','',
                 '','','','','',
                 '','','','','']

photo_folder_path = fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\Photos"

list_of_photos = get_file_paths(photo_folder_path)

list_of_intro_memes = [fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\Intro Memes\Picture1.jpg",
                       fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\Intro Memes\Picture2.jpg"]

list_of_personality_memes = [fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\personality memes\picture 1.jpg",
                             fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\personality memes\Picture4.jpg"]

closing_memes = [fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\closing meme\Picture1.jpg",
                             fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\closing meme\Picture2.jpg"]


#Add metric functions
metric_method_dict = {'Contacts': run_contacts,
                      'Visits': run_visits,
                      'Qualifications': run_qualifications,
                      'Asks': run_asks,
                      'Booked': run_booked}

def flow_function(dictionary,
                  music_list,
                  video_list,
                  photo_list,
                  color_list,
                  intro_meme_path,
                  personality_meme_path,
                  closing_memes_path,
                  font1,
                  font2,
                  username):
    render_video_list = []

    ## find the highest percentile metrics for each gift officer
    metric_percentile_list = [('Contacts', dictionary['Contacts: Percentile']),
                            ('Visits', dictionary['Visits: Percentile']),
                            ('Qualifications', dictionary['Qualifications: Percentile']),
                            ('Asks', dictionary['Asks: Percentile']),
                            ('Booked', dictionary['Booked: Percentile'])]
    metric_percentile_list_sorted = sorted(metric_percentile_list, key=lambda x: x[1], reverse=True)

    # call start series
    start_list, full_duration = start_series(dictionary, color_list[0],
                                             font1,
                                             font2,
                                             intro_meme_path,
                                             username)
    render_video_list = render_video_list + start_list
    print('Start Duration = ' + str(full_duration))

    # call first metric
    print(metric_percentile_list_sorted[0][0])
    first_list, full_duration = metric_method_dict['Contacts'](dictionary,
                                                                                        color_list[1],
                                                                                        full_duration-1,
                                                                                        font1,
                                                                                        photo_list[:10])
    render_video_list = render_video_list + first_list
    print('Metric 1 Duration = ' + str(full_duration))

    # call archetype
    personality_test = Archetype(dictionary,
                                 color_list[2],
                                 full_duration-1,
                                 font1,
                                 personality_meme_path,
                                 username)
    archetype_list =  personality_test.video_list
    full_duration = personality_test.stop_duration_sum
    render_video_list = render_video_list + archetype_list

    print('Archetype Duration = ' + str(full_duration))
    # call second metric
    print(metric_percentile_list_sorted[1][0])
    second_list, full_duration = metric_method_dict['Visits'](dictionary,
                                                                                         color_list[3],
                                                                                         full_duration-1,
                                                                                         gotham_medium_font,
                                                                                         photo_list[10:])
    render_video_list = render_video_list + second_list
    print('Metric 2 Duration = ' + str(full_duration))
    # call close
    close_list, full_duration = close(dictionary,color_list[4], font1, closing_memes_path,full_duration-1)
    render_video_list = render_video_list + close_list

    #Is the goal to render the video within the function or have the video render out of the function?
    return render_video_list

def replace_nan_by_type(df):
    for col in df.columns:
        if df[col].dtype == np.number:
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna('')
    return df

df_go_metrics = replace_nan_by_type(df_go_metrics)


# Filtering down just to gift officers who have names
#df_go_metrics = df_go_metrics[df_go_metrics['Final Name'].isin(visit_names2)]

random_number = random.randint(0, len(df_go_metrics.index))

today = datetime.today().strftime('%d %H %M')


for i in range(0,len(df_go_metrics.index)):

# for i in error_numbers2:
#for i in range(random_number, random_number+1):

    go_dict = df_go_metrics.iloc[i].to_dict()

    go_name = go_dict['Final Name']
    print(go_name)

    logging.info(str(go_name) + ' ' + str(i))

    random_colors = random.sample(uchicago_background_colors, 5)
    random_photos = random.sample(list_of_photos, 20)
    random_videos = random.sample(list_of_videos, 2)
    random_audio = random.sample(list_of_music, 1)
    random_intro_meme = random.sample(list_of_intro_memes, 1)
    random_personality_meme = random.sample(list_of_personality_memes, 1)
    random_closing_meme = random.sample(closing_memes, 1)

    logging.info(f"Start {go_name}'s render")
    print(str(i) +" " + str(go_name))

    print(random_colors)
    print(random_photos)
    print(random_videos)
    print(random_audio)
    print(random_intro_meme)
    print(random_personality_meme)
    print(random_closing_meme)

    try:
        video_list = CompositeVideoClip(flow_function(go_dict,
                                                      random_audio,
                                                      random_videos,
                                                      random_photos,
                                                      random_colors,
                                                      random_intro_meme[0],
                                                      random_personality_meme[0],
                                                      random_closing_meme[0],
                                                      gotham_medium_font,
                                                      garamond_regular,
                                                      username))

        # insert music
        print(random_audio[0])
        mp4_duration = video_list.duration
        audio_clip1 = (AudioFileClip(random_audio[0])
                 .with_start(0)
                 .with_effects([afx.AudioLoop(duration=mp4_duration)])
                       )
        video_list2 = video_list.with_audio(audio_clip1)

        # render video

        video_list2.write_videofile(fr"C:\Users\{username}\Box\ARD Year in Review 2024\{go_name}.mp4")
        #video_list2.write_videofile(
        #   fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\Rendered Videos\{today} {go_name}.mp4")

        logging.info(f"End {go_name}'s render")

    except Exception as e:
            logging.info(f"End {go_name}'s render - Error {e}")

    except ZeroDivisionError as e:
            logging.info(f"End {go_name}'s render - Error {e}")

