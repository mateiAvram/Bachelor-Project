import os
from dotenv import load_dotenv

import itertools

import isodate
import time
import datetime
import numpy as np
from dateutil import parser
from enum import Enum

import pandas as pd
from googleapiclient.discovery import build

from server.model.enum import VideoCategories

# # Initial helper functions
# def generate_combinations(input_list):
#     combinations = []
#     for r in range(1, 3):  # Generate combinations of length 1 to 3
#         combinations.extend(itertools.combinations(input_list, r))
#     return combinations

# input_list = [category.value for category in VideoCategories]
# result = generate_combinations(input_list)
# for r in result:
#     category = ''
#     for e in r:
#         category += e
#         category += ' '
#     category = category[:-1]
#     print(category)

# print(f'Total: ({len(result)})')

##################################################################
# Importing classes here because imports are not very functional
##################################################################

class Video:
    def __init__(self, video_id = None, title = None, categories = None, duration = None, tags = None, publish_date = None):
        self.video_id = video_id
        self.title = title
        self.categories = categories
        self.duration = duration
        self.tags = tags

        if publish_date == None:
            self.publish_date = datetime.datetime.now()
        else:
            self.publish_date = datetime.datetime.strptime(publish_date, '%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return f"Video(id={self.video_id}, title='{self.title}', categories='{self.categories}', duration='{self.duration}', tags='{self.tags}' publish_date='{self.publish_date}')"

    def to_dict(self):
        return {
            'video_id': self.video_id,
            'title': self.title,
            'categories': self.categories,
            'duration': self.duration,
            'tags': self.tags,
            'publish_date': self.publish_date.strftime('%Y-%m-%d %H:%M:%S') if self.publish_date else None
        }

    def generate_vector(self):
        vector = {category.value: 0 for category in VideoCategories}
        for category in self.categories.split(' '):
            vector[category] = 1
        return ' '.join(str(v) for v in np.array(list(vector.values())))

class VideoCategories(Enum):
    ARTS = 'arts'
    BIOLOGY = 'biology'
    BUSINESS = 'business'
    CHEMISTRY = 'chemistry'
    COMPUTER_SCIENCE = 'computer_science'
    LITERATURE = 'literature'
    MATHEMATICS = 'mathematics'
    MUSIC = 'music'
    PHYSICS = 'physics'
    PSYCHOLOGY = 'psychology'

##################################################################

subjects_dict = {
    # "arts": ["SchaeferArt", "willkempartschool", "The Drawing Database", "Proko", "Art Prof: Visual Art Essentials"],
    # "biology": ["SciShow", "Crash Course Biology", "MinuteEarth", "Nature League", "Biointeractive"],
    # "business": ["Valuetainment", "GaryVee", "TED-Ed Business", "The Financial Diet", "MBA Bullshit"],
    # "chemistry": ["Periodic Videos", "NileRed", "Tyler DeWitt", "Crash Course Chemistry", "CENtral Science"],
    # "computer_science": ["Computerphile", "The Coding Train", "Khan Academy Computing", "Net Ninja", "Traversy Media"],
    "literature": ["Crash Course Literature", "The School of Life", "TED-Ed Literature", "Learn English with Gill", "Thug Notes"],
    # "mathematics": ["3Blue1Brown", "Numberphile", "Mathologer", "Mathantics", "MindYourDecisions"],
    "music": ["Paul Davids", "Pianote", "Rick Beato", "The-Art-of-Guitar", "Adam Neely"],

    # "physics": ["Physics Girl", "MinutePhysics", "Veritasium", "Smarter Every Day", "PBS Space Time"],
    "psychology": ["Psych2Go", "The Psych Show", "Crash Course Psychology", "BrainCraft", "SciShow Psych"],
    "biology chemistry physics": ["Medlife Crisis", "Chubbyemu", "Healthcare Triage", "JJ Medicine", "Dr. Mike"],  # MEDICINE
    "mathematics physics": ["NASA", "PBS Space Time", "Fraser Cain", "The Bad Astronomer", "Anton Petrov"],  # ASTRONOMY
    # "computer_science mathematics": ["Lex Fridman", "Two Minute Papers", "3Blue1Brown", "Khan Academy Computing", "Sentdex"],  # ARTIFICIAL INTELLIGENCE
    # "biology chemistry": ["23andMe", "The Genetic Genealogist", "Learn Genetics", "Geno 2.0 Next Generation", "Khan Academy Biology"],  # GENETICS
    # "business mathematics": ["Marginal Revolution University", "Khan Academy Economics", "Crash Course Economics", "The School of Life Economics", "EconplusDal"],  # ECONOMICS
    # "arts business": ["Neil Patel", "GaryVee", "HubSpot", "Marketing 360", "Brian Dean (Backlinko)"],  # MARKETING

    # "business psychology": ["Harvard Business Review", "London Business School", "Stanford Graduate School of Business", "The Futur", "EntreLeadership"],  # MANAGEMENT
    # "mathematics music": ["Numberphile", "3Blue1Brown", "Vi Hart", "David Bennett Piano", "Adam Neely"],  # (music + mathematics)
    # "music psychology": ["Adam Neely", "12tone", "Dr. K's Psychobook", "Neurotransmissions", "Music and the Brain"],  # (music + psychology)
    # "arts psychology": ["The School of Life", "TED-Ed", "Psych2Go", "Art Therapy", "How to ADHD"]  # (arts + psychology)
}

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

def get_videos(channel_name, wanted_tags, unwanted_tags, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # First retrieve channel id
    channel_response = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id,snippet',
        maxResults=1
    ).execute()
    
    if not channel_response['items']:
        return []
    channel_id = channel_response['items'][0]['id']['channelId']

    # Search for videos by channel id
    search_response = youtube.search().list(
        channelId=channel_id,
        type='video',
        part='id,snippet',
        maxResults=max_results,
        videoDuration='short',
        videoEmbeddable='true'
    ).execute()

    # Collecting and filtering the results
    videos = []
    for search_result in search_response.get('items', []):
        if len(videos) < 10:
            video_id = search_result['id']['videoId']
            video_response = youtube.videos().list(part='snippet,contentDetails', id=video_id).execute()
            
            # Filtering
            duration_iso = video_response['items'][0]['contentDetails']['duration']
            duration_seconds = isodate.parse_duration(duration_iso).total_seconds()
            duration_ms = int(duration_seconds * 1000)

            tags = video_response['items'][0]['snippet'].get('tags', [])
            tags_str = ', '.join(tags).lower()
            
            if duration_ms <= 60000 and (True if all(tag not in tags for tag in unwanted_tags) else False) and (True if all(tag in tags for tag in wanted_tags) else False):

                # Getting final information
                title = video_response['items'][0]['snippet']['title']

                publish_date = video_response['items'][0]['snippet']['publishedAt']
                publish_date_parsed = parser.parse(publish_date)
                publish_date_str = publish_date_parsed.strftime('%Y-%m-%d %H:%M:%S')

                videos.append({
                    'id': video_id,
                    'title': title,
                    'duration': duration_ms,
                    'tags': tags_str,
                    'publish_date': publish_date_str,
                    'url': f'https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&controls=1&loop=1&playlist={video_id}&enablejsapi=1&widgetid=1'
                })
        else:
            continue
    
    return videos



total_channels = len(subjects_dict.keys()) * 5
print(f'total searches: ({total_channels})')

tags = [category.value for category in VideoCategories]
results = {
    key: [] for key in subjects_dict.keys()
}

print('\n--started searching--\n')
for key, channel_list in subjects_dict.items():

    wanted_tags = []
    unwanted_tags = tags[:]
    for tag in key.split(' '):
        wanted_tags.append(tag)
        unwanted_tags.remove(tag)
    
    print(f'category: {key}')
    for channel_name in channel_list:
        print(f'searching for: {channel_name}')
        results[key].extend(get_videos(channel_name, wanted_tags, unwanted_tags))
    print()
print('--finished searching--\n')

columns = ['video_id', 'title', 'categories', 'duration', 'tags', 'publish_date', 'vector']
df = pd.DataFrame(columns = columns)

total_videos = 0
for key, value in results.items():
    print(f'{key}: ({len(value)})')
    total_videos += len(value)
    for v in value:
        video = Video(
            video_id = v['id'],
            title = v['title'],
            categories = key,
            duration = v['duration'],
            tags = v['tags'],
            publish_date = v['publish_date']
        )
        vector = video.generate_vector()
        entry = video.to_dict()
        entry['vector'] = vector
        entry_df = pd.DataFrame([entry])
        df = pd.concat([df, entry_df], ignore_index=True)
print('---')
print(f'Total: ({total_videos})\n')

##################################################################
# Modify for next sets
index = 1
##################################################################

csv_file_path = f'videos_set_{index}.csv'
df.to_csv(csv_file_path, index=False)
print('--saved--')
