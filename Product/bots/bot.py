import requests
import numpy as np
from enum import Enum

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

class Bot:
    URL = 'http://127.0.0.1:5000/'

    def __init__(self, bot_id, categories, levels):
        self.bot_id = bot_id
        self.session = requests.Session()
        self.categories = {c.value: 1 for c in VideoCategories}
        for c, i in zip(categories, levels):
            self.categories[c] = i
        self.vector=''
    
    def __repr__(self):
        return f"Bot(id={self.bot_id}, categories='{self.categories}')"

    def generate_vector(self):
        vector = {key: 0.1 for key in self.categories.keys()}
        for key, value in self.categories.items():
            if value == 2:
                print(f'category: {key}')
                vector[key] = 0.30
                continue
            if value == 3:
                print(f'category: {key}')
                vector[key] = 0.50
                continue
            if value == 4:
                print(f'category: {key}')
                vector[key] = 0.70
                continue
            if value == 5:
                print(f'category: {key}')
                vector[key] = 0.90
        self.vector = ' '.join(str(v) for v in np.array(list(vector.values())))

    def create_account(self):
        payload = {
            "account": {
                "username": f"bot{self.bot_id}",
                "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "role": "user"
            },

            "categories": ' '.join(self.categories)
        }
        
        endpoint = 'signup'
        response = self.session.post(url=Bot.URL + endpoint, json=payload)
        if response.status_code == 200:
            print(f'Bot{self.bot_id}: sign-up successfull')
            return 0
        print(f'Bot{self.bot_id}: sign-up failed')
        return -1

    def log_in(self):
        payload = {
            "username": f"bot{self.bot_id}",
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
        }
        endpoint = 'login'
        response = self.session.post(url=Bot.URL + endpoint, json=payload)
        if response.status_code == 200:
            print(f'Bot{self.bot_id}: log-in successfull')
            return 0
        print(f'Bot{self.bot_id}: log-in failed')
        return -1

    def request_videos(self):
        endpoint = 'request_videos'
        response = self.session.get(url=Bot.URL + endpoint)
        if response.status_code == 200:
            print(f'Bot{self.bot_id}: videos request successfull')
            data = response.json()
            return data.get('videos')
        print(f'Bot{self.bot_id}: videos request failed')
        return -1

    def send_data(self, payload):
        endpoint = 'user_action'
        response = self.session.post(url=Bot.URL + endpoint, json=payload)
        if response.status_code == 200:
            print(f'Bot{self.bot_id}: watch data sent successfully')
            return 0
        print(f'Bot{self.bot_id}: watch data failed')
        return -1
        
