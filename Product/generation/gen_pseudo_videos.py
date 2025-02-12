import os
from dotenv import load_dotenv
import random
import itertools
import isodate
import time
from dateutil import parser
from datetime import datetime, timedelta
import pandas as pd
from enum import Enum
import numpy as np

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

class Video:
    def __init__(self, video_id = None, title = None, categories = None, duration = None, tags = None, publish_date = None, vector = ''):
        self.video_id = video_id
        self.title = title
        self.categories = categories
        self.duration = duration
        self.tags = tags

        if publish_date == None:
            self.publish_date = datetime.now()
        else:
            self.publish_date = datetime.strptime(publish_date, '%Y-%m-%d %H:%M:%S')
        self.vector = vector

    def __repr__(self):
        return f"Video(id={self.video_id}, title='{self.title}', categories='{self.categories}', duration='{self.duration}', tags='{self.tags}' publish_date='{self.publish_date}')"

    def to_dict(self):
        return {
            'video_id': self.video_id,
            'title': self.title,
            'categories': self.categories,
            'duration': self.duration,
            'tags': self.tags,
            'publish_date': self.publish_date.strftime('%Y-%m-%d %H:%M:%S') if self.publish_date else None,
            'vector': self.vector
        }

    def generate_vector(self):
        vector = {category.value: 0 for category in VideoCategories}
        # vector[self.categories] = 1
        for category in self.categories.split(' '):
            vector[category] = 1
        video_vector = np.array([v for v in list(vector.values())])
        norm = np.linalg.norm(video_vector)
        video_vector = video_vector / norm
        self.vector = ' '.join(str(v) for v in video_vector)
        


def generate_random_date():
    end_date = datetime(2024, 1, 1)
    start_date = end_date - timedelta(days=365 * 10)
    
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date

random.seed(42)

##################################################################
# Version 1
# Initial helper functions
def generate_combinations(input_list):
    combinations = []
    for r in range(1, 4):  # Generate combinations of length 1 to 3
        combinations.extend(itertools.combinations(input_list, r))
    return combinations

input_list = [category.value for category in VideoCategories]
result = generate_combinations(input_list)
##################################################################

##################################################################
# # Version 2 generate more accurate videos according to existing fields
# def generate_combinations(input_list):
#     combinations = []
#     for r in range(1, len(input_list) + 1):
#         combinations.extend(itertools.combinations(input_list, r))
#     return combinations

# classes = ['biology chemistry', 'arts literature music psychology', 'business literature', 'mathematics physics', 'biology chemistry psychology', 'computer_science physics', 'biology chemistry mathematics physics', 'computer_science mathematics physics', 'business psychology', 'literature psychology']

# result = []
# for c in classes:
#     combination_list = generate_combinations(c.split(' '))
#     for e in combination_list:
#         if not e in result:
#             result.append(e)
##################################################################

##################################################################
# # Version 3 videos belong to only a single category
# result = [category.value for category in VideoCategories]
##################################################################

for r in result:
    print(r)

print(f'Total: ({len(result)})')

keys = [' '.join(r) for r in result]
# keys = [r for r in result]

columns = ['video_id', 'title', 'categories', 'duration', 'tags', 'publish_date', 'vector']
df = pd.DataFrame(columns = columns)

print('\n--generating videos--\n')
index = 1
for key in keys:
    for _ in range(28):
        video = Video(
                video_id = index,
                title = f'Video Title {index}',
                categories = key,
                duration = random.randint(30, 60) * 1000,
                tags = '',
                publish_date = generate_random_date().strftime("%Y-%m-%d %H:%M:%S")
            )
        video.generate_vector()
        index+=1

        entry = video.to_dict()
        entry_df = pd.DataFrame([entry])
        df = pd.concat([df, entry_df], ignore_index=True)

print('\n--finished generating--\n')
print(f'Total: ({index - 1})\n')

print(df.head(10))

##################################################################
# Modify for next sets
index = 1
##################################################################

csv_file_path = f'videos_set_comb_2.csv'
df.to_csv(csv_file_path, index=False)
print('--saved--')