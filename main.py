from time import sleep
from flask import Flask, request, abort, render_template,jsonify
import requests
import json

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
    URIAction,
    PostbackTemplateAction,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction,
    MessageAction
)
from linebot.exceptions import LineBotApiError

from model.model import checkAccount, getLineProfile

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'Ay9oSCj6k3ZWIzToj+9ZQ313CSPLgnLgqUfutaz8Y3+ZbF7A9LaEbb9amLCPeszT/aPodrVHeNXXK13pteYf1Dnyx56dbgK3uOiPzg33N7nzKEttAmCml9pFxDcX0iPQXulAIIk4eIa6o+P6DIV9XQdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = 'e0e86fec93bdf9b0de1f647ecd050b25'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/test")
def test():
    template = render_template('index.html')
    # print(template)
    return template

@app.route("/line_check", methods=['POST'])
def line_check():
    """ access token 獲取line user id """
    # sleep(5)
    body = request.get_data(as_text=True)
    return getLineProfile(body)

@app.route("/account_check", methods=['POST'])
def account_check():
    """ 登入身分證、密碼確認 """
    body = request.get_data(as_text=True)
    return checkAccount(body)
    
@app.route("/register_check", methods=['POST'])
def register_check():
    """ 註冊資訊確認，並傳送otp號碼 """
    body = request.get_data(as_text=True)
    
@app.route("/otp_check", methods=['POST'])
def otp_check():
    """ otp比對，有效期限預設300s """
    body = request.get_data(as_text=True)

@app.route("/", methods=['GET'])
def get():
    # logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
    body = request.get_data(as_text=True)
    print(body)
    return 'get test'

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

    u_a = URIAction(
        label='uri',
        uri='https://liff.line.me/1656766770-y9GzVJpG'
    )

    if in_text == 'test':
        pass
    elif in_text == 'button':
        b_a = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackAction(
                        label='postback',
                        display_text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message',
                        text='message text'
                    ),
                    URIAction(
                        label='uri',
                        uri='https://liff-playground.netlify.app/'
                    ),
                    URIAction(
                        label='uri',
                        uri='https://liff.line.me/1656766770-y9GzVJpG'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, b_a)
    elif in_text == 'broadcast':
        pass
        # line_bot_api.broadcast(TextSendMessage(text='Hello World!'))
    elif in_text == 'create':
        # u_a = URIAction(label='Go to line.me', uri='https://line.me')
        # print(u_a)
        p_a = PostbackTemplateAction(
            label='postback',
            display_text='postback text',
            data='action=buy&itemid=1'
        )
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=2500, height=843),
            selected=False,
            name="Nice richmenu",
            chat_bar_text="Tap here",
            areas=[RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
                action=u_a)]
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
