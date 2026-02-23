from flask import Flask
import redis
import os

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 0))

app = Flask(__name__)

redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

@app.route("/")
def home():
    return "Welcome to my multi-container Flask application!"

@app.route("/count")
def count():
    visits = redis_client.incr("visits")
    return f"You have visited this page {visits} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)