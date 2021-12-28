from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'HdC4dE9CXPr4rZUbSzKGrvWMC34RLhTch+g8LTNBttPoMu8WybRUYPXssmvaUXOfq30SzhMKSCWjeDxlJ41q7IoxIALmt1QmzCsjE7u+WCryZKgeWEtRUTcD3X7ZXizAky2ik/uVa6GqGMZMeNLr249PbdgDzCFqoOLOYbqAITQ='
YOUR_CHANNEL_SECRET = '11ad239b794460554b7b26e2dce7b615'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
    # line_bot_api.reply_message(reply_token, TextSendMessage(text='Hello World!'))