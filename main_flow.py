import os

user_path = os.path.expanduser("~")
username = os.path.basename(user_path)

import pandas as pd
from Scripts.start_sequence import start_series
from Scripts.main import YearInReview

# fonts (Gotham is not a default font)
gotham_medium_font = r"C:\Windows\Fonts\Gotham-Medium.otf"
garamond_regular = r"C:\Windows\Fonts\GARABD.ttf"

# Background colors in RGB
uchicago_background_colors = [(172,203,249), # air
                              (74,102,172), # lake
                              (98,157,209), #sky
                              (0, 89, 132), # case blue
                              (127, 143, 169),  # steel
                              (20, 63, 106),  # navy
                              (90, 162, 174),  # sea moss
                               (52, 119, 178),  # ocean
    ]

# colors for the pi charts for asked and booked in RGB
graph_colors =[
    (255, 165, 0),    # Pure Orange
    (255, 215, 0),    # Gold
    (255, 140, 0),    # Dark Orange
    (255, 180, 70),   # Light Orange
    (255, 100, 0)     # Deep Orange
]

# create a path to your mustic
music_folder_path = r".\Sample Files\music"
    # fr"C:\Users\{username}\Box\Prospect Management & Financial Analytics\PM Analytics and Reporting\Deliverables\24.10.28 ARD Wrapped 24\music"

# create a list for each of the meme locations
list_of_intro_memes = [r".\Sample Files\data science\Screenshot 2025-04-01 164517.png",
                       r".\Sample Files\data science\Screenshot 2025-04-01 164557.png"]
list_of_personality_memes = [r".\Sample Files\personality memes\picture 1.jpg",
                             r".\Sample Files\personality memes\Picture4.jpg",]
closing_memes = [r".\Sample Files\fundraising\62f6889d87ee5be53047b5c2_meme-5.jpg",
                 r".\Sample Files\fundraising\62f6888076402766f7190845_meme-2.jpg"]

# Where do you want the videos to be created?
output_path = fr"C:\Users\{username}\Downloads\Test Video"

# Dataframe that contains productivity details for each gift officer.
# The code will iterate through this list
df_go_metrics = pd.read_csv(fr'.\Sample Files\Sample Dataframe.csv')


# Archetype Folder
# Included in the Archetype Folder is a PSD that can be used to edit this file
# folder also needs to include a locator and a question png
path = r".\Sample Files\archetype_images2"

# Path to Pheonix Logo used in Archetype
phoenix_path = r".\Sample Files\archetype_images2\UChicago_Phoenix_Outlined_1Color_White_RGB.png"

# image
images = [r'\1st layer.png',
                  r'\2nd layer.png',
                  r'\3rd layer.png',
                  r'\4th layer.png',
                  r'\5th layer.png']

#Run this class to generate the videos. Render times will vary based on computer capabilities
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