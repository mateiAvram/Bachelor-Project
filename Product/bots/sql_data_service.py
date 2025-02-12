import sqlite3
from bot import Bot

class SqlDataService:
    def __init__(self):
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_2.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_3.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_4.db'
        # self.path = '/home/para/Desktop/Project A/Product/database_experiment_5.db'
        self.path = '/home/para/Desktop/Project A/Product/database_experiment_multiple.db'

        # Bots Constants
        self.table_bots = 'bots'
        self.field_bot_id = 'id'
        self.field_bot_username = 'username'
        self.field_bot_vector = 'vector'

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
    # Bots Functions
    ##################################################################

    def get_usernames(self):
        query = f"SELECT {self.field_bot_username} FROM {self.table_bots}"
        print(query)

        result = self.execute_query(query)
        results = []
        for r in result:
            results.append(r[0])
        return results

    def insert_bot(self, new_bot: Bot):
        query = f"INSERT INTO {self.table_bots} ({self.field_bot_username}, {self.field_bot_vector}) VALUES ('bot{new_bot.bot_id}', '{new_bot.vector}')"

        print(query)

        result = self.execute_query(query)
        return result

    ##################################################################