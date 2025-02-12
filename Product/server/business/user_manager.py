from model.user import User, UserAction
from data.sql_data_service import SqlDataService

class UserManager:

    @staticmethod
    def get_user(id):
        data_service = SqlDataService()
        return data_service.get_user_by_id(id)

    @staticmethod
    def insert_user(data):
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        new_user = User(username = username, password = password, role = role)
        data_service = SqlDataService()
        return data_service.insert_user(new_user)

    @staticmethod
    def record_action(data, user_id):
        video_id = data.get('video_id')
        action_type = data.get('action_type')
        duration = data.get('duration')
        new_user_action = UserAction(user_id = user_id, video_id = video_id, action_type = action_type, duration = duration)
        data_service = SqlDataService()
        data_service.insert_user_action(new_user_action)

        # Fetching necessary information
        video = data_service.get_video_by_id(video_id)

        print(f'Video duration: {video.duration}')
        print(f'Client duration: {duration}')

        # All durations are calculated in ms
        watch_percentage = (100 * (int(duration) - 1000)) / int(video.duration)
        print(f'watch percentage: {watch_percentage}')

        # Update user vector
        user = data_service.get_user_by_id(user_id)
        user.update_vector(video.vector, action_type, watch_percentage)

        # Store the updated vector
        return data_service.update_user(user)