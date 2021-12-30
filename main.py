from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FlexSendMessage,
    RichMenu,
    RichMenuSize,
    RichMenuBounds,
    RichMenuResponse,
    RichMenuArea,
    URIAction
)
from linebot.exceptions import LineBotApiError

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'Ay9oSCj6k3ZWIzToj+9ZQ313CSPLgnLgqUfutaz8Y3+ZbF7A9LaEbb9amLCPeszT/aPodrVHeNXXK13pteYf1Dnyx56dbgK3uOiPzg33N7nzKEttAmCml9pFxDcX0iPQXulAIIk4eIa6o+P6DIV9XQdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = 'e0e86fec93bdf9b0de1f647ecd050b25'

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
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    print(event.reply_token)
    print(TextSendMessage(text=event.message.text))
    in_text = event.message.text
    if in_text == 'test':
        pass
    elif in_text == 'broadcast':
        pass
        # line_bot_api.broadcast(TextSendMessage(text='Hello World!'))
    elif in_text == 'create':
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=2500, height=843),
            selected=False,
            name="Nice richmenu",
            chat_bar_text="Tap here",
            areas=[RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
                action=URIAction(label='Go to line.me', uri='https://line.me'))]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print(rich_menu_id)
        file_path = './test.jpg'
        content_type = "image/png"
        with open(file_path, 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)
        line_bot_api.set_default_rich_menu(rich_menu_id)
    else:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

    # try:
    #     line_bot_api.push_message('<to>', TextSendMessage(text='Hello World!'))
    # except LineBotApiError as e:
    #     print(e)

    # line_bot_api.reply_message(reply_token, TextSendMessage(text='Hello World!'))
