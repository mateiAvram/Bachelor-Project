import numpy as np
from datetime import datetime
from model.enum import VideoCategories

class Video:
    def __init__(self, video_id = None, title = None, categories = None, duration = None, tags = None, publish_date = None, vector = ''):
        self.video_id = video_id
        self.title = title
        self.categories = categories
        self.duration = duration
        self.tags = tags
        self.vector = vector

        if publish_date == None:
            self.publish_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.publish_date = datetime.strptime(publish_date, '%Y-%m-%d %H:%M:%S')


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
    
    @staticmethod
    def convert_to_numpy(vector: str):
        return np.array([float(v) for v in vector.split(' ')])

    @staticmethod
    def convert_to_string(vector: np.array):
        return ' '.join(str(v) for v in vector)

    @staticmethod
    def cosine_similarity(video_vector, user_vector):
        video_vector = Video.convert_to_numpy(video_vector)
        user_vector = Video.convert_to_numpy(user_vector)
        dot_product = np.dot(video_vector, user_vector)
        norm_video = np.linalg.norm(video_vector)
        norm_user = np.linalg.norm(user_vector)
        similarity = dot_product / (norm_video * norm_user)
        return similarity

    def generate_vector(self):
        vector = {category.value: 0 for category in VideoCategories}
        for category in self.categories.split(' '):
            vector[category] = 1
        self.vector = ' '.join(str(v) for v in np.array(list(vector.values())))