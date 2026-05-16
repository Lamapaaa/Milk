import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='public', static_url_path='')

DB_FILE = 'database.json'

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading DB: {e}")

    return {
        "profile": {
            "username": "Tonas_",
            "role": "ВЛАДЕЛЕЦ",
            "status": "Лучший сервер!",
            "badges": ["⚡", "</>", "💎"],
            "faction": None
        },
        "comments": [
            { "author": "Blackslime", "text": "Крутой дизайн!", "date": "Сегодня в 12:00" },
            { "author": "altamly", "text": "Всё работает идеально", "date": "Вчера в 15:30" }
        ]
    }

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db = load_db()

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/profile/<username>', methods=['GET'])
def get_profile(username):
    # For this demo, we use a single profile
    return jsonify(db['profile'])

@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    data = request.json
    profile = db['profile']

    if 'username' in data:
        profile['username'] = data['username']
    if 'status' in data:
        profile['status'] = data['status']
    if 'faction' in data:
        profile['faction'] = data['faction']

    save_db(db)
    return jsonify({ "status": "success", "profile": profile })

@app.route('/api/comments', methods=['GET'])
def get_comments():
    return jsonify(db['comments'])

@app.route('/api/comments', methods=['POST'])
def add_comment():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({ "error": "Text is required" }), 400

    new_comment = {
        "author": data.get('author', 'Аноним'),
        "text": text,
        "date": datetime.now().strftime("%d.%m.%Y, %H:%M")
    }
    db['comments'].insert(0, new_comment)
    save_db(db)
    return jsonify(new_comment), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
