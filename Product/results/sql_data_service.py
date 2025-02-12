import sqlite3

class SqlDataService:
    def __init__(self):
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_2.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_3.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_4.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_5.db'
        self.path = '/home/para/Desktop/Project A/Product/database_experiment_multiple.db'

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
    # Functions
    ##################################################################

    def get_profiling_results(self):
        query = """
        SELECT b.id, b.username, b.vector, u.vector
        FROM bots b
        JOIN users u
        ON b.username = u.username
        """

        result = self.execute_query(query)
        return result

    def get_recommendation_results(self):
        query = """
        SELECT u.username, b.vector, v.video_id, v.categories, ua.type, ua.duration AS action_duration, v.duration as video_duration
        FROM users_actions ua
        JOIN users u ON ua.user_id = u.id
        JOIN videos v ON v.video_id = ua.video_id
        LEFT JOIN bots b ON u.username = b.username;
        """

        result = self.execute_query(query)
        return result

    def get_training_set(self):
        query = """
        SELECT * 
        FROM videos
        ORDER BY publish_date DESC
        LIMIT 500
        """

        result = self.execute_query(query)
        return result

    ##################################################################