import os
import sys

user_path = os.path.expanduser("~")
username = os.path.basename(user_path)

import pandas as pd
import numpy as np
import re
import xlsxwriter
from datetime import date, datetime
from great_tables import GT
from moviepy import *
from main import YearInReview
import random
from matplotlib import font_manager
import textwrap
import matplotlib.pyplot as plt
from moviepy import *

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

music_folder_path = fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\music"

list_of_intro_memes = [fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\Intro Memes\Picture1.jpg",
                       fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\Intro Memes\Picture2.jpg"]

list_of_personality_memes = [fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\personality memes\picture 1.jpg",
                             fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\personality memes\Picture4.jpg"]

closing_memes = [fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\closing meme\Picture1.jpg",
                             fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\closing meme\Picture2.jpg"]


output_path = fr"C:\Users\{username}\Downloads"

df_go_metrics = pd.read_csv(fr'C:\Users\{username}\Downloads\Sample Dataframe.csv')

graph_colors = [(234, 170, 0), (222, 124, 0), (120, 157, 74), (39, 93, 56), (0, 115, 150), (89, 49, 95), (164, 52, 58)]

phoenix_path = fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\UChicago_Phoenix_Outlined_1Color_White_RGB.png"

path = fr'C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\archetype_images2'
# folder also needs to include a locator and a question png

images = [r'\1st layer.png',
                  r'\2nd layer.png',
                  r'\3rd layer.png',
                  r'\4th layer.png',
                  r'\5th layer.png']

YearInReview(music_folder_path=music_folder_path,
             background_colors=uchicago_background_colors,
             photo_folder_path=music_folder_path,
             title_font=gotham_medium_font,
             body_font=garamond_regular,
             intro_memes=list_of_intro_memes,
             personality_type_memes=list_of_personality_memes,
             output_path=output_path,
             closing_memes=closing_memes,
graph_colors2=graph_colors,
             productivity_data_frame=df_go_metrics,
             logo=phoenix_path,
             archetype_path = path,
             archetype_images= images,
             )