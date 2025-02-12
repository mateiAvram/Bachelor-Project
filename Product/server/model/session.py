import uuid
import datetime

class Session:
    def __init__(self, user_id, expiry_time=None):
        self.session_id = str(uuid.uuid4())
        self.user_id = user_id

        if expiry_time == None:
            # Creating 30 min session
            self.expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        else:
            # Setting the expiry_time
            self.expiry_time = datetime.datetime.strptime(expiry_time, '%Y-%m-%d %H:%M:%S.%f')

    def __repr__(self):
        return f"session(id={self.session_id}, user_id='{self.user_id}', expiry_time='{self.expiry_time}')"

    def is_valid(self):
        return datetime.datetime.now() < self.expiry_time