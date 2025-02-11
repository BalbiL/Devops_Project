import os
import redis
from flask import *
import socket


# Check if the app is running in Docker
def is_running_in_docker():
    try:
        with open("/proc/self/cgroup") as f:
            return any("docker" in line for line in f)
    except FileNotFoundError:
        return False

# Dynamically retrieve Redis host based on the environment
if is_running_in_docker():
    # Inside Docker, Redis will be the service name in Docker Compose
    redis_host = os.getenv('REDIS_HOST', 'redis')
else:
    # On the VM, connect to Redis via the VM's IP or localhost
    redis_host = os.getenv('REDIS_HOST', 'localhost') 
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Redis connection

r = redis.StrictRedis(host=redis_host, port=6379, decode_responses=True)





@app.route('/')
def index():
    # Supprimer l'email de l'utilisateur sélectionné de la session
    session.pop('selected_user', None)

    # Récupérer l'email de l'utilisateur sélectionné dans la session
    selected_user_email = session.get('selected_user', None)

    # Si un utilisateur est sélectionné, récupérer ses détails
    if selected_user_email:
        selected_user = r.hgetall(f"user:{selected_user_email}")
        # Formater le nom et surnom pour mettre le surnom entre parenthèses
        selected_user_info = {
            'name': selected_user.get('name'),
            'surname': selected_user.get('surname'),
            'email': selected_user.get('email')
        }
    
        selected_user_info['formatted_name'] = f"{selected_user_info['name']} ({selected_user_info['surname']}) - {selected_user_info['email']}"
    else:
        selected_user_info = None

    return render_template('temp1.html', selected_user=selected_user_info)

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

@app.route('/api/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    email = data.get('email')

    # Check if the user exists
    if not r.exists(f"user:{email}"):
        return jsonify({"error": "User not found!"}), 404

    # Delete the user from Redis
    r.delete(f"user:{email}")
    return jsonify({"message": "User deleted successfully!"}), 200

@app.route('/api/select_user', methods=['POST'])
def select_user():
    data = request.json
    email = data.get('email')

    # Store selected user's email in the session
    session['selected_user'] = email
    return jsonify({"message": "User selected successfully!"}), 200

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    email = data.get('email')
    message = data.get('message')

    if not email or not message:
        return jsonify({'error': 'Email and message are required'}), 400

    # Vérifier si l'utilisateur existe
    user = r.hgetall(f"user:{email}")
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Ajouter le message à la liste Redis
    message_data = {
        'email': email,
        'message': message
    }
    r.rpush('messages', json.dumps(message_data))  # Ajouter à la fin de la liste

    return jsonify({'success': True}), 200

@app.route('/api/get_messages', methods=['GET'])
def get_messages():
    # Récupérer tous les messages
    messages = r.lrange('messages', 0, -1)
    formatted_messages = [json.loads(msg) for msg in messages]

    # Ajouter le nom de l'utilisateur à chaque message
    for msg in formatted_messages:
        user_data = r.hgetall(f"user:{msg['email']}")
        msg['name'] = user_data.get('name', 'Unknown User')

    return jsonify(formatted_messages), 200

@app.route('/api/delete_message', methods=['POST'])
def delete_message():
    data = request.json
    email = data.get('email')
    message_content = data.get('message')

    if not email or not message_content:
        return jsonify({'error': 'Email and message content are required'}), 400

    # Récupérer tous les messages
    messages = r.lrange('messages', 0, -1)

    # Chercher et supprimer le message correspondant
    for msg in messages:
        decoded_msg = json.loads(msg)
        if decoded_msg['email'] == email and decoded_msg['message'] == message_content:
            r.lrem('messages', 1, msg)  # Supprimer 1 occurrence
            return jsonify({'success': True}), 200

    return jsonify({'error': 'Message not found'}), 404


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
