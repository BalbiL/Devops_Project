from flask import *
import redis

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def index():
    # Serve the HTML page
    return render_template('temp1.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    # Retrieve all users from Redis
    users = [r.hgetall(key) for key in r.keys('user:*')]
    return jsonify(users)

@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')

    # Check if email already exists
    if r.exists(f"user:{email}"):
        return jsonify({"error": "This email is already registered!"}), 400

    # Save user to Redis
    r.hset(f"user:{email}", mapping={
        'name': name,
        'surname': surname,
        'email': email
    })
    return jsonify({"message": "User added successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
