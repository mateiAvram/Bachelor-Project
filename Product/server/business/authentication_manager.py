import numpy as np
from model.enum import VideoCategories
from model.user import User
from model.session import Session
from business.user_manager import UserManager
from data.sql_data_service import SqlDataService

class AuthenticationManager:

    @staticmethod
    def signup(data):
        account_data = data.get('account')
        data_service = SqlDataService()

        username = account_data.get('username')
        
        # Checking is username is unique
        usernames = data_service.get_usernames()
        if username in usernames:
            raise Exception('username not available')
        
        password = account_data.get('password')
        role = account_data.get('role')
        new_user = User(username = username, password = password, role = role)

        # Creating user vector based on preferences
        # categories = data.get('categories').split(' ')
        categories = '' # Un-comment for blind recommendation
        
        new_user.generate_vector(categories)

        # Inserting new vuser
        data_service.insert_user(new_user)
        return 0

    # TODO Session bug (multiple for same user)
    @staticmethod
    def login(data):
        username = data.get('username')
        password = data.get('password')
        data_service = SqlDataService()

        # Checking credentials
        user = data_service.get_user_by_username(username)
        if username != user.username:
            raise Exception('incorrect username')

        if password != user.password:
            raise Exception('incorrect password')

        # # Create session
        # session = Session(user_id = user.user_id)
        # data_service.insert_session(session)
        # return session.session_id, user.user_id
        return user.user_id
    