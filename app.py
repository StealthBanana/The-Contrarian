from flask import Flask

# Configure applications
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>,"


