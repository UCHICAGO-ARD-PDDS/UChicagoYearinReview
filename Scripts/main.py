import os
import pandas as pd
import numpy as np
import re
import xlsxwriter
import win32com.client as win32
from datetime import date, datetime
from great_tables import GT
from moviepy import *
from Scripts.start_sequence import start_series
from Scripts.archetype_sequence2 import Archetype
from Scripts.close_sequence2 import close
from Scripts.metric_clips import *
from Scripts.metric_flows import *
import random
# from pyfonts import load_font

class YearInReview():
    # Add metric functions
    metric_method_dict = {'Contacts': run_contacts,
                          'Visits': run_visits,
                          'Qualifications': run_qualifications,
                          'Asks': run_asks,
                          'Booked': run_booked}

    def __init__(self,
                 music_folder_path,
                 background_colors,
                 photo_folder_path,
                 title_font,
                 body_font,
                 intro_memes,
                 personality_type_memes,
                 closing_memes,
                 output_path,
                 productivity_data_frame,
                 graph_colors2,
                 logo,
                 archetype_path,
                 archetype_images):
        print("init")
        self.list_of_music = self.get_file_paths(music_folder_path)
        self.uchicago_background_colors = background_colors
        self.list_of_photos = self.get_file_paths(photo_folder_path)
        self.gotham_medium_font = title_font
        self.garamond_regular = body_font

        df_go_metrics = productivity_data_frame
        df_go_metrics = self.replace_nan_by_type(df_go_metrics)

        # Filtering down just to gift officers who have names
        # df_go_metrics = df_go_metrics[df_go_metrics['Final Name'].isin(visit_names2)]

        random_number = random.randint(0, len(df_go_metrics.index))

        today = datetime.today().strftime('%d %H %M')
        list_of_intro_memes = intro_memes
        list_of_personality_memes = personality_type_memes


        list_of_videos = ['','']

        for i in range(0, len(df_go_metrics.index)):
            print(i)
            # for i in error_numbers2:
            # for i in range(random_number, random_number+1):

            go_dict = df_go_metrics.iloc[i].to_dict()

            go_name = go_dict['Final Name']
            print(go_name)

            random_colors = random.sample(self.uchicago_background_colors, 5)
            random_photos = random.sample(self.list_of_photos, 0)
            random_videos = random.sample(list_of_videos, 2)
            random_audio = random.sample(self.list_of_music, 1)
            random_intro_meme = random.sample(list_of_intro_memes, 1)
            random_personality_meme = random.sample(list_of_personality_memes, 1)
            random_closing_meme = random.sample(closing_memes, 1)

            print(str(i) + " " + str(go_name))

            print(random_colors)
            print(random_photos)
            print(random_videos)
            print(random_audio)
            print(random_intro_meme)
            print(random_personality_meme)
            print(random_closing_meme)

            username = ""

            video_list = CompositeVideoClip(self.flow_function(go_dict,
                                                          random_audio,
                                                          random_videos,
                                                          random_photos,
                                                          random_colors,
                                                          random_intro_meme[0],
                                                          random_personality_meme[0],
                                                          random_closing_meme[0],
                                                          self.gotham_medium_font,
                                                          self.garamond_regular,
                                                          username,
                                                               graph_colors2,
                                                               logo,
                                                               archetype_path,
                                                               archetype_images
                                                               ))

            # insert music
            print(random_audio[0])
            mp4_duration = video_list.duration
            audio_clip1 = (AudioFileClip(random_audio[0])
                           .with_start(0)
                           .with_effects([afx.AudioLoop(duration=mp4_duration)])
                           )
            video_list2 = video_list.with_audio(audio_clip1)

            # render video

            video_list2.write_videofile(output_path + r"\\"+go_name+".mp4")

    def get_file_paths(self, directory):
        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths

    def flow_function(self,
                      dictionary,
                      music_list,
                      video_list,
                      photo_list,
                      color_list,
                      intro_meme_path,
                      personality_meme_path,
                      closing_memes_path,
                      font1,
                      font2,
                      username,
                      graph_colors,
                      logo,
                      archetype_path,
                      archetype_images):
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
                                                 username,
                                                 logo)
        render_video_list = render_video_list + start_list
        print('Start Duration = ' + str(full_duration))

        # call first metric
        print(metric_percentile_list_sorted[0][0])
        first_list, full_duration = self.metric_method_dict['Contacts'](dictionary,
                                                                   color_list[1],
                                                                   full_duration - 1,
                                                                   font1,
                                                                   photo_list[:10],
                                                                    graph_colors)
        render_video_list = render_video_list + first_list
        print('Metric 1 Duration = ' + str(full_duration))

        # call archetype
        personality_test = Archetype(dictionary,
                                     color_list[2],
                                     full_duration - 1,
                                     font1,
                                     personality_meme_path,
                                     username,
                                     archetype_path,
                                     archetype_images
                                     )
        archetype_list = personality_test.video_list
        full_duration = personality_test.stop_duration_sum
        render_video_list = render_video_list + archetype_list

        print('Archetype Duration = ' + str(full_duration))
        # call second metric
        print(metric_percentile_list_sorted[1][0])
        second_list, full_duration = self.metric_method_dict['Visits'](dictionary,
                                                                  color_list[3],
                                                                  full_duration - 1,
                                                                  self.gotham_medium_font,
                                                                  photo_list[10:],
                                                                    graph_colors)
        render_video_list = render_video_list + second_list
        print('Metric 2 Duration = ' + str(full_duration))
        # call close
        close_list, full_duration = close(dictionary, color_list[4], font1, closing_memes_path, full_duration - 1)
        render_video_list = render_video_list + close_list

        # Is the goal to render the video within the function or have the video render out of the function?
        return render_video_list

    def replace_nan_by_type(self, df):
        for col in df.columns:
            if df[col].dtype == np.number:
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna('')
        return df








