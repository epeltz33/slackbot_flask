import os
from flask import Flask
from slack import WebClient

app = Flask(__name__)

slack_web_client = WebClient(token=os.environ.get("SLACKBOT_TOKEN"))
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
