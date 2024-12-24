import os
import redis
from flask import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dynamically retrieve Redis host
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.StrictRedis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def index():
    return render_template('temp1.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    users = [r.hgetall(key) for key in r.keys('user:*')]
    return jsonify(users)

@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')

    if r.exists(f"user:{email}"):
        return jsonify({"error": "This email is already registered!"}), 400

    r.hset(f"user:{email}", mapping={
        'name': name,
        'surname': surname,
        'email': email
    })
    return jsonify({"message": "User added successfully!"}), 200

@app.route('/api/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    email = data.get('email')

    if not r.exists(f"user:{email}"):
        return jsonify({"error": "User not found!"}), 404

    r.delete(f"user:{email}")
    return jsonify({"message": "User deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
