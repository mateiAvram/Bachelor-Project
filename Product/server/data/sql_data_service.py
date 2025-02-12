import sqlite3
from model.user import User, UserAction
from model.video import Video
from model.session import Session

class SqlDataService:
    def __init__(self):
        # self.path = '/home/para/Desktop/Project A/Product/database_showcase.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_2.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_3.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_4.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_5.db'
        self.path = '/home/para/Desktop/Project A/Product/database_experiment_multiple.db'

        # User Constants
        self.table_users = 'users'
        self.field_user_id = 'id'
        self.field_user_username = 'username'
        self.field_user_password = 'password'
        self.field_user_role = 'role'
        self.field_user_vector = 'vector'

        # UserAction Constants
        self.table_ua = 'users_actions'
        self.field_ua_id = 'id'
        self.field_ua_user_id = 'user_id'
        self.field_ua_video_id = 'video_id'
        self.field_ua_type = 'type'
        self.field_ua_timestamp = 'timestamp'
        self.field_ua_duration = 'duration'

        # Session Constants
        self.table_sessions = 'sessions'
        self.field_session_id = 'id'
        self.field_session_user_id = 'user_id'
        self.field_session_expiry_time = 'expiry_time'

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

            if cursor.description is not None:
                results = cursor.fetchall()
                return results
            else:
                conn.commit()
                return 0

        except sqlite3.Error as e:
            print("SQLite error:", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    ##################################################################


    ##################################################################
    # User Functions
    ##################################################################

    def get_usernames(self):
        query = f"SELECT {self.field_user_username} FROM {self.table_users}"
        print(query)

        result = self.execute_query(query)
        results = []
        for r in result:
            results.append(r[0])
        return results

    def insert_user(self, new_user: User):
        query = f"INSERT INTO {self.table_users} ({self.field_user_username}, {self.field_user_password}, {self.field_user_role}, {self.field_user_vector}) VALUES ('{new_user.username}', '{new_user.password}', '{new_user.role}', '{new_user.vector}')"

        print(query)

        result = self.execute_query(query)
        return result

    def get_user_by_id(self, user_id):
        query = f"SELECT * FROM {self.table_users} WHERE {self.field_user_id} = '{user_id}'"
        print(query)
        
        result = self.execute_query(query)
        if result != []:
            user = result[0]
            return User(user_id = user[0], username = user[1], password = user[2], role = user[3], vector = user[4])
        return User()

    def get_user_by_username(self, username):
        query = f"SELECT * FROM {self.table_users} WHERE {self.field_user_username} = '{username}'"
        print(query)
        
        result = self.execute_query(query)
        if result != []:
            user = result[0]
            return User(user_id = user[0], username = user[1], password = user[2], role = user[3], vector = user[4])
        return User()

    def update_user(self, user: User):
        query = f"""UPDATE {self.table_users} SET {self.field_user_username} = '{user.username}', {self.field_user_password} = '{user.password}', {self.field_user_role} = '{user.role}', {self.field_user_vector} = '{user.vector}' WHERE {self.field_user_id} = '{user.user_id}'"""
        print(query)

        result = self.execute_query(query)
        return result

    # TODO
    def delete_user(self, username):
        return

    ##################################################################

    ##################################################################
    # User Action Functions
    ##################################################################

    def insert_user_action(self, new_action: UserAction):
        query = f"INSERT INTO {self.table_ua} ({self.field_ua_user_id}, {self.field_ua_video_id}, {self.field_ua_type}, {self.field_ua_timestamp}, {self.field_ua_duration}) VALUES ('{new_action.user_id}', '{new_action.video_id}', '{new_action.action_type}', '{new_action.timestamp}', '{new_action.duration}')"

        print(query)

        result = self.execute_query(query)
        return result

    # TODO
    def update_user_action(self, action: UserAction):
        return

    # TODO
    def delete_user_action(self, action_id):
        return

    ##################################################################


    ##################################################################
    # Video Functions
    ##################################################################
    
    def get_video_by_id(self, video_id):
        query = f"SELECT * FROM {self.table_videos} WHERE {self.field_video_id} = '{video_id}'"
        print(query)
        
        result = self.execute_query(query)
        if result != []:
            video = result[0]
            return Video(video_id = video[0], title = video[1], categories = video[2], duration = video[3], tags = video[4], publish_date = video[5], vector = video[6])
        return Video()

    # def get_recommended_videos(self, user_id, categories):

    #     # # Constructing the Where condition clause
    #     condition = " OR ".join(f"{self.field_video_categories} LIKE '%{category}%'" for category in categories)

    #     query = f"""SELECT * FROM {self.table_videos} WHERE ({condition}) 
    #                 AND {self.field_video_id} NOT IN (
    #                     SELECT {self.field_ua_video_id} FROM {self.table_ua} WHERE {self.field_ua_user_id} = '{user_id}' 
    #                     AND (strftime('%s', {self.field_ua_timestamp}) > strftime('%s', 'now', '-30 days'))
    #                 )
    #                 ORDER BY {self.field_video_publish_date} DESC
    #                 LIMIT 18
    #             """
    #     print(query)

    #     results = self.execute_query(query)
    #     return results

    # Return video function experiment
    def get_videos(self, user_id, offset):

        query = f"""WITH unseen_videos AS (
            SELECT v.*
            FROM {self.table_videos} v
            LEFT JOIN {self.table_ua} ua
            ON v.{self.field_video_id} = ua.{self.field_ua_video_id}
            AND ua.{self.field_ua_user_id} = {user_id}
            WHERE ua.{self.field_ua_video_id} IS NULL
        )
        SELECT * 
        FROM unseen_videos
        ORDER BY {self.field_video_publish_date} DESC
        LIMIT 50 OFFSET {offset}
        """

        # ids = ', '.join(checked_ids + watched_ids)
        # query = f"""SELECT * FROM {self.table_videos} WHERE {self.field_video_id} NOT IN ({ids}) ORDER BY {self.field_video_publish_date} DESC LIMIT 50"""
        print(query)

        results = self.execute_query(query)
        # print('results: ')
        # print(results)
        return results

    def get_watched_videos_by_id(self, user_id):
        query = f"""SELECT {self.field_ua_video_id} FROM {self.table_ua} WHERE {self.field_ua_user_id} = '{user_id}' AND (strftime('%s', {self.field_ua_timestamp}) > strftime('%s', 'now', '-30 days')) LIMIT 1000"""
        print(query)

        results = self.execute_query(query)

        ids = []
        for r in results:
            ids.append(str(r[0]))
        return ids

    def insert_video(self, new_video: Video):
        query = f"INSERT INTO {self.table_videos} ({self.field_video_id}, {self.field_video_title}, {self.field_video_categories}, {self.field_video_duration}, {self.field_video_tags}, {self.field_video_publish_date}, {self.field_video_vector}) VALUES ('{new_video.video_id}', '{new_video.title}', '{new_video.categories}', '{new_video.duration}', '{new_video.tags}', '{new_video.publish_date}', '{new_video.vector}')"
        print(query)

        result = self.execute_query(query)
        return result

    # TODO
    def delete_video(self, video_id):
        return

    ##################################################################


    ##################################################################
    # Session Functions
    ##################################################################

    def insert_session(self, new_session: Session):
        query = f"INSERT INTO {self.table_sessions} ({self.field_session_id}, {self.field_session_user_id}, {self.field_session_expiry_time}) VALUES ('{new_session.session_id}', '{new_session.user_id}', '{new_session.expiry_time}')"
        print(query)

        result = self.execute_query(query)
        return result

    # TODO
    def delete_session(self, session_id):
        return

    ##################################################################