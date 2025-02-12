from model.video import Video
from model.user import User
from model.enum import VideoCategories
from data.sql_data_service import SqlDataService

class VideoManager:

    # TODO
    @staticmethod
    def insert_video(data):
        return

    @staticmethod
    def get_videos(user_id):
        data_service = SqlDataService()

        # Getting user vector
        user = data_service.get_user_by_id(user_id)
        
        # Getting watched videos ids
        watched_videos_ids = data_service.get_watched_videos_by_id(user_id)

        videos = []
        # Giving some time for the algorithm to build the user vector
        if len(watched_videos_ids) < 500:
            # print('IF')
            retrieved_videos = data_service.get_videos(user_id, 0)
            for v in retrieved_videos:
                # print(v)
                if len(videos) == 10:
                    continue

                video = Video(
                    video_id = v[0], 
                    title = v[1], 
                    categories = v[2], 
                    duration = v[3], 
                    tags = v[4], 
                    publish_date = v[5],
                    vector = v[6]
                )
                videos.append(video.to_dict())
            return videos

        threshold = 0.9
        offset = 0
        retrieved_videos = data_service.get_videos(user_id, offset)
        if retrieved_videos == []:
            return []

        
        while len(videos) < 10 and retrieved_videos != []:

            added_videos = []
            for v in retrieved_videos:
                if len(videos) == 10:
                    continue

                video = Video(
                    video_id = v[0], 
                    title = v[1], 
                    categories = v[2], 
                    duration = v[3], 
                    tags = v[4], 
                    publish_date = v[5],
                    vector = v[6]
                )
                similarity = Video.cosine_similarity(video.vector, user.vector)
                # print(similarity)
                if similarity >= threshold:
                    videos.append(video.to_dict())
                    added_videos.append(v)

            for v in added_videos:
                retrieved_videos.remove(v)

            if len(videos) == 10:
                continue

            if threshold > 0.4:
                threshold -= 0.1
                continue

            threshold = 0.9
            offset += 50
            retrieved_videos = data_service.get_videos(user_id, offset)

        return videos
    