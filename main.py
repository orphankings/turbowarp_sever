import json
from flask import Flask, request, jsonify

app = Flask(__name__) # 架設伺服器

def load_players():
    try:
        with open("data/players.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_players():
    with open("data/players.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

players = load_players()

@app.route("/") # 路徑 
def hello():
    return "sever working"

@app.route("/register", methods=["POST"]) # 註冊
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    
    if username in players:
        return jsonify({"ok": False, "msg": "user exists"})
    
    players[username] = {
        "password": password
    }

    save_players()
    
    return jsonify({"ok": True})

@app.route("/login", methods=["POST"]) # 登入
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    
    if username not in players:
        return jsonify({"ok": False, "msg": "no such user"})
    
    if players[username]["password"] != password:
        return jsonify({"ok": False, "msg": "wrong password"})

    return jsonify({"ok": True})

@app.route("/update", methods=["POST"]) # 玩家資料更新
def update():
    data = request.json
    username = data["username"]
    value = data.get("value")
    
    if username not in players:
        return jsonify({"ok": False, "msg": "error"})
    
    players[username]["value"] = value
    save_players()
    return jsonify({"ok": True})



