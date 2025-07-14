from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
app.config['SONG_FOLDER'] = './songs'

# Simulated user database
users = {"admin": "1234"}

# Simulated token store (in memory for now)
tokens = {}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        token = os.urandom(16).hex()
        tokens[token] = username
        return jsonify({"message": "Login success", "token": token})
    return jsonify({"error": "Invalid credentials"}), 403

@app.route('/download', methods=['GET'])
def download():
    token = request.headers.get("Authorization")
    if token not in tokens:
        return jsonify({"error": "Unauthorized"}), 401

    filename = 'song1.txt'  # demo song
    return send_from_directory(app.config['SONG_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['SONG_FOLDER'], exist_ok=True)
    with open('./songs/song1.txt', 'w') as f:
        f.write("This is the content of the demo song.")
    app.run(debug=True)
