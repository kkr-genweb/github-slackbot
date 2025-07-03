import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Create your app with bot token
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Example listener: reply to @bot mentions
@app.event("app_mention")
def handle_app_mention_events(event, say):
    user = event["user"]
    say(f"Hi there, <@{user}>! :wave:")

# Run the app in Socket Mode
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()