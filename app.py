import os
import random
from slack import WebClient
from flask import Flask
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)
slack_web_client = WebClient(token=os.environ.get("SLACKBOT_TOKEN"))  # allows us to interact with slack client

MESSAGE_TEMPLATE = {
    "type": "section",
    "text": {
        "type": "mrkdwn",  # markdown
        "text": (
            "Hello, I'm a bot! :tada:\n\n"
            "*How can I help you?*"
        ),
    },
}


@slack_events_adapter.on("message")  # listens for messages
def message(payload):
    event = payload.get("event", {})

    text = event.get("text")

    if "flip a coin" in text.lower():
        channel_id = event.get("channel")
        random_int = random.randint(0,1)
        if random_int == 0:
            results = "Heads"
        else:
            results = "Tails"
        message = f"Flipping a coin: {results}"

        MESSAGE_TEMPLATE["text"]["text"] = message
        message_to_send = {"channel": channel_id, "blocks": [MESSAGE_TEMPLATE]}

        return slack_web_client.chat_postMessage(**message_to_send)






if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
