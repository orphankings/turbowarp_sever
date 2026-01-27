from flask import Flask

app = Flask(__name__) # 架設伺服器

@app.route("/") # 路徑 
def hello():
    return "OK"
