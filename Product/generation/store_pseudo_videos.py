import sqlite3
from enum import Enum
from datetime import datetime
import pandas as pd

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
        for category in self.categories.split(' '):
            vector[category] = 1
        self.vector = ' '.join(str(v) for v in np.array(list(vector.values())))

class SqlDataService:
    def __init__(self):
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment.db'
        self.path = '/home/para/Desktop/Project A/Product/database_experiment_multiple.db'

        # Video Constants
        self.table_videos = 'videos'
        self.field_video_id = 'video_id'
        self.field_video_title = 'title'
        self.field_video_categories = 'categories'
        self.field_video_duration = 'duration'
        self.field_video_tags = 'tags'
        self.field_video_publish_date = 'publish_date'
        self.field_video_vector = 'vector'

    ##################################################################
    # General Functions
    ##################################################################

    def execute_query(self, query):
        conn = None
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return results
            else:
                conn.commit()
                return 0

        except sqlite3.Error as e:
            print("SQLite error:", e)
        finally:
            if conn:
                conn.close()

    ##################################################################

    ##################################################################
    # Video Functions
    ##################################################################

    def insert_video(self, new_video: Video):
        query = f"INSERT INTO {self.table_videos} ({self.field_video_id}, {self.field_video_title}, {self.field_video_categories}, {self.field_video_duration}, {self.field_video_tags}, {self.field_video_publish_date}, {self.field_video_vector}) VALUES ('{new_video.video_id}', '{new_video.title}', '{new_video.categories}', '{new_video.duration}', '{new_video.tags}', '{new_video.publish_date}', '{new_video.vector}')"
        # print(query)

        result = self.execute_query(query)
        return result

    ##################################################################

file_path = 'videos_set_comb_1.csv'
# file_path = 'videos_set_single_1.csv'
df = pd.read_csv(file_path)

print('\n--started storing videos--')
data_service = SqlDataService()

for index, row in df.iterrows():
    video = Video(
        video_id = row['video_id'], 
        title = row['title'], 
        categories = row['categories'], 
        duration = row['duration'], 
        tags = '' if pd.isna(row['tags']) else row['tags'], 
        publish_date = row['publish_date'],
        vector = row['vector']
    )
    data_service.insert_video(video)

print('--finished storing videos--')