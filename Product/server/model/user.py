from datetime import datetime
import numpy as np
from model.enum import VideoCategories

class User:
    def __init__(self, user_id = None, username = None, password = None, role = None, vector = ''):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.vector = vector
    
    def __repr__(self):
        return f"Account(id={self.user_id}, username='{self.username}', password='{self.password}', role='{self.role}', vector='{self.vector}')"

    @staticmethod
    def convert_to_numpy(vector: str):
        return np.array([float(v) for v in vector.split(' ')])

    @staticmethod
    def convert_to_string(vector: np.array):
        formatted_vector_list = [f'{num:.7f}' for num in vector]
        return ' '.join(formatted_vector_list)
        # return ' '.join(str(v) for v in vector)

    @staticmethod
    def calc_adaptive_learning_rates(user_vector, base_rate = 0.05, max_rate = 0.15):
        # TO-DO maybe do adaptive learning rates
        return np.array([0.1 for v in user_vector])

    def generate_vector(self, categories):
        vector = {category.value: 0 for category in VideoCategories}
        for category in categories:
            vector[category] = 0.5
        self.vector = ' '.join(str(v) for v in np.array(list(vector.values())))

    def update_vector(self, video_vector, action_type, watch_percentage):
        user_vector = User.convert_to_numpy(self.vector)
        video_vector = User.convert_to_numpy(video_vector)
        rates = User.calc_adaptive_learning_rates(user_vector)

        # Setting constant increments for like and dislike action
        like = 0.1
        dislike = -0.05
        watch_time = 0.06
        if watch_percentage < 0.75:
            watch_time = 0.04
        if watch_percentage < 0.5:
            watch_time = 0.02
        if watch_percentage < 0.25:
            watch_time = -0.01

        # Adujusting vector for action type
        for index in range(len(video_vector)):
            if video_vector[index] != 0:
                if action_type == 'like':
                    user_vector[index] += like * rates[index]
                elif action_type == 'dislike':
                    user_vector[index] += dislike * rates[index]
                user_vector[index] += watch_time * rates[index]

        norm = np.linalg.norm(user_vector)
        user_vector = user_vector / norm

        self.vector = User.convert_to_string(user_vector)

class UserAction:
    def __init__(self, action_id = None, user_id = None, video_id = None, action_type = None, timestamp = None, duration = None):
        self.action_id = action_id
        self.user_id = user_id
        self.video_id = video_id
        self.action_type = action_type
        self.duration = duration

        if timestamp == None:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return f"Action(user_id='{self.user_id}', video_id='{self.video_id}', action_type='{self.action_type}')"