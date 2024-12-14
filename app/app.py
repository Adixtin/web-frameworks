from flask import Flask, request, jsonify
from typing import List, Dict, Optional

app = Flask(__name__)

users_db: List[Dict] = []


def find_user_by_id(user_id: int) -> Optional[Dict]:
    return next((user for user in users_db if user['id'] == user_id), None)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the User Management Application!', 200

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users_db), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = find_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return '', 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'name' not in data or 'lastname' not in data:
        return '', 400

    new_id = len(users_db) + 1

    new_user = {
        'id': new_id,
        'name': data['name'],
        'lastname': data['lastname']
    }

    users_db.append(new_user)
    return '', 201


@app.route('/users/<int:user_id>', methods=['PATCH'])
def partial_update_user(user_id: int):
    user = find_user_by_id(user_id)
    if not user:
        return '', 404

    data = request.get_json()

    if not data or (len(data) > 1 or not ('name' in data or 'lastname' in data)):
        return '', 400

    if 'name' in data:
        user['name'] = data['name']
    if 'lastname' in data:
        user['lastname'] = data['lastname']

    return '', 204


@app.route('/users/<int:user_id>', methods=['PUT'])
def full_update_user(user_id: int):
    data = request.get_json()

    if not data or 'name' not in data or 'lastname' not in data:
        return '', 400

    user = find_user_by_id(user_id)

    if user:
        user['name'] = data['name']
        user['lastname'] = data['lastname']
    else:
        new_user = {
            'id': user_id,
            'name': data['name'],
            'lastname': data['lastname']
        }
        users_db.append(new_user)

    return '', 204


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    global users_db
    initial_length = len(users_db)
    users_db = [user for user in users_db if user['id'] != user_id]

    if len(users_db) < initial_length:
        return '', 204
    else:
        return '', 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)