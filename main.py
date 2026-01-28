import json
from flask import Flask, request, jsonify

app = Flask(__name__) # 架設伺服器

if __name__ == "__main__":
    # Render 會提供 PORT 環境變數
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


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
    req = request.json
    username = req["username"]
    password = req["password"]
    
    if username in players:
        return jsonify({"ok": False, "msg": "user exists"})
    
    players[username] = {
        "password": password, # 密碼
        "data":{
            "level": 1,
            "xp": 0,
            
            "money": 0,
            "gold": 0,
            "diamond": 0,
            
            "stage": {
                "main": {
                    "current": 1,
                    "clear": []
                },
                "bosstower": {
                    "current": 1,
                    "clear": []
                },
                "trail": {
                    "current": 1,
                    "clear": []
                }
            },
            
            "hero": [],
            "equipment": [],
            "tactics": [],
            "stone": [],
            "item": [],
            
            "activity": {},
            "gacha": {},
            
            "task":[]
        }
    }

    save_players()
    
    return jsonify({"ok": True})

@app.route("/login", methods=["POST"]) # 登入
def login():
    req = request.json
    username = req["username"]
    password = req["password"]
    
    if username not in players:
        return jsonify({"ok": False, "msg": "no such user"})
    
    if players[username]["password"] != password:
        return jsonify({"ok": False, "msg": "wrong password"})

    return jsonify({"ok": True})

@app.route("/update", methods=["POST"]) # 玩家資料更新
def update():
    req = request.json
    username = req["username"]
    data = req.get("data")
    
    if username not in players:
        return jsonify({"ok": False, "msg": "error"})
    
    players[username]["data"] = data
    save_players()
    return jsonify({"ok": True})



