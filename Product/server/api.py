import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from business.authentication_manager import AuthenticationManager
from business.user_manager import UserManager
from business.video_manager import VideoManager

app = Flask(__name__, static_folder='../../Product/client/web')
CORS(app, supports_credentials=True)

# Static file serving
@app.route('/')
def serve_index():
    return send_from_directory('../client/web', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('assets'):
        return send_from_directory('../client/assets', path[len('assets/'):])
    elif path.startswith('style'):
        return send_from_directory('../client/style', path[len('style/'):])
    else:
        return send_from_directory('../client/web', path)

# Authentication API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    am = AuthenticationManager()
    try:
        # session_id, user_id = am.login(data)
        user_id = am.login(data)

        data = {'message': 'OK'}
        resp = jsonify(data)
        # resp.set_cookie('session_id', session_id)
        resp.set_cookie('user_id', str(user_id))
        return resp

    except Exception as e:
        data = {'message': e.args[0]}
        resp = jsonify(data)
        return resp


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    am = AuthenticationManager()
    try:

        am.signup(data)

        data = {'message': 'OK'}
        resp = jsonify(data)
        return resp

    except Exception as e:
        data = {'message': e.args[0]}
        resp = jsonify(data)
        return resp

@app.route('/request_videos', methods=['GET'])
def request_videos():
    vm = VideoManager()
    try:

        cookie = request.cookies.get('user_id', 'None')
        videos = vm.get_videos(cookie)

        data = {
            'message': 'OK',
            'videos': videos
            }
        resp = jsonify(data)
        return resp

    except Exception as e:
        data = {'message': e.args[0]}
        resp = jsonify(data)
        return resp

@app.route('/user_action', methods=['POST'])
def user_action():
    data = request.json

    # TODO
    # Should update to also verify if the user is authenticated
    um = UserManager()
    try:
        
        cookie = request.cookies.get('user_id', 'None')
        um.record_action(data, cookie)

        data = {'message': 'OK'}
        resp = jsonify(data)
        return resp

    except Exception as e:
        data = {'message': e.args[0]}
        resp = jsonify(data)
        return resp

if __name__ == '__main__':
    app.run(debug = True)