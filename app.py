from flask import Flask, request, abort, jsonify

# Line Bots related
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Google API related
import gspread
from google.oauth2.service_account import Credentials

import os
app = Flask(__name__)
# ============= Google sheets related: Your Channel Access Token and Channel Secret from LINE Developers Console ============
# Path to your service account key file
# Get the absolute path to the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the service account JSON file
SERVICE_ACCOUNT_FILE = os.path.join(current_directory, 'client_secret.json')

# Define the scope for accessing Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Authorize and create a client for accessing Google Sheets
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)


def get_specific_cell_value(row, column):
    try:
        # Google Sheet ID and the name of the sheet tab
        SHEET_ID = '1oZ_lf6CKXgeVNizEfYxoCa6U0RPpzEIfwAklnMtEQWc'
        SHEET_NAME = 'Yun_Show'

        # Open the Google Sheet
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(SHEET_NAME)

        # Get all values in the specific column (e.g., 'A' or 'B')
        column_index = ord(column.upper()) - ord('A') + 1

        # Get the value at the specified row and column
        cell_value = worksheet.cell(row, column_index).value

        # Get all value at the column
        # column_values = worksheet.col_values(column_index)

        # Return the column values as JSON
        return column_values

    except Exception as e:
        return jsonify({"error": str(e)})



# ============= Line Bots Related: Your Channel Access Token and Channel Secret from LINE Developers Console ============
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
        # Get the values from column 'B'
        column_values = get_specific_cell_value(1, 'B')

        # Join the values to send as a response
        # reply_message = TextSendMessage(text=f"Value in cell B1: {column_values}")
        reply_message = TextSendMessage(text=f"Value in cell B1: {column_values}")
        line_bot_api.reply_message(event.reply_token, reply_message)
    else:
        # Optionally handle other cases
        reply_message = TextSendMessage(text="Please send '1' to get a response.")
        line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6000, debug=True)
