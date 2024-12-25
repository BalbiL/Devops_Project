from flask import Flask, jsonify, request
import redis

app = Flask(__name__)

# Connexion à Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

@app.route("/")
def hello():
    return "Hello, Redis World!"

@app.route("/set", methods=["POST"])
def set_value():
    key = request.json.get("key")
    value = request.json.get("value")
    redis_client.set(key, value)
    return jsonify({"message": f"Key '{key}' set to '{value}'"}), 200

@app.route("/get/<key>", methods=["GET"])
def get_value(key):
    value = redis_client.get(key)
    if value is None:
        return jsonify({"error": "Key not found"}), 404
    return jsonify({"key": key, "value": value}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)