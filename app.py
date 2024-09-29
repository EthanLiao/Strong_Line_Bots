from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# Your Channel Access Token and Channel Secret from LINE Developers Console
# LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "YOUR_CHANNEL_ACCESS_TOKEN")
# LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "YOUR_CHANNEL_SECRET")

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "RnAnoy9C2ko+vv9o7nAZbGsq6sioV8/Pvwbe0pIME97CdQiG4SBnI5+ue9xmCiobtzzTbWeIKB9mK5ka4ceY5SO5oLpbrFkIBtZ6mgqGChuOjABGsKTye3I83Uq6OBtGMKhbYpPIjTo5jtFUzIs0QwdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "6826e79b8f8b0928c258836eff06e75e")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # Get the request signature from the headers
    signature = request.headers['X-Line-Signature']

    # Get the request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Define how to handle text messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # Check if the message is '1'
    if user_message == '1':
        # Reply the same message '1'
        reply_message = TextSendMessage(text=user_message)
        line_bot_api.reply_message(event.reply_token, reply_message)
    else:
        # Optionally handle other cases
        reply_message = TextSendMessage(text="Please send '1' to get a response.")
        line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6000, debug=True)
