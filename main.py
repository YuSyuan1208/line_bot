from time import sleep
from flask import Flask, request, abort, render_template, jsonify
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
    MessageAction,
    CarouselTemplate,
    CarouselColumn
)
from linebot.exceptions import LineBotApiError

from model.model import checkAccount, checkOtp, checkRegister, getLineProfile

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'Ay9oSCj6k3ZWIzToj+9ZQ313CSPLgnLgqUfutaz8Y3+ZbF7A9LaEbb9amLCPeszT/aPodrVHeNXXK13pteYf1Dnyx56dbgK3uOiPzg33N7nzKEttAmCml9pFxDcX0iPQXulAIIk4eIa6o+P6DIV9XQdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = 'e0e86fec93bdf9b0de1f647ecd050b25'

MY_LINE_ID = 'Ub95da38ba9b7324f35940beca4f7d01e'

TEST_GROUP_ID = 'Ce5cc6bfdfbc457ffd77dcee848343a18'

# MY_LINE_ID = 'Uf346eebe9f4e39d1d4dd56219a3d9877'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

text_template_message = TextSendMessage(text='Hello World!')
print(text_template_message)

carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://example.com/item1.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message1',
                        text='message text1'
                    ),
                    URIAction(
                        label='uri1',
                        uri='http://example.com/1'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageAction(
                        label='message2',
                        text='message text2'
                    ),
                    URIAction(
                        label='uri2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
)

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
    return checkRegister(body)


@app.route("/otp_check", methods=['POST'])
def otp_check():
    """ otp比對，有效期限預設300s """
    body = request.get_data(as_text=True)
    return checkOtp(body)


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


@app.route("/broadcast_test", methods=['GET'])
def broadcast_test():
    line_bot_api.broadcast(TextSendMessage(text='Hello World!'))
    return 'broadcast test'


@app.route("/push_message", methods=['GET'])
def push_message():
    to = MY_LINE_ID
    re = line_bot_api.push_message(to, b_a)
    print(re)
    return 'push_message test'


@app.route("/get_followers_ids", methods=['GET'])
def get_followers_ids():
    test_result = line_bot_api.get_followers_ids()
    print(test_result.user_ids)
    return 'get_followers_ids test'


@app.route("/get_insight_message_delivery", methods=['GET'])
def get_insight_message_delivery():
    insight = line_bot_api.get_insight_message_delivery('20191231')
    print(insight.api_broadcast)
    return 'get_insight_message_delivery test'


@app.route("/get_insight_followers", methods=['GET'])
def get_insight_followers():
    insight = line_bot_api.get_insight_followers('20191231')
    print(insight.followers)
    return 'get_insight_followers test'


@app.route("/get_insight_demographic", methods=['GET'])
def get_insight_demographic():
    insight = line_bot_api.get_insight_demographic()
    print(insight.genders)
    return 'get_insight_demographic test'


@app.route("/bot_info", methods=['GET'])
def bot_info():
    bot_info = line_bot_api.get_bot_info()
    print(bot_info.display_name)
    print(bot_info.user_id)
    print(bot_info.basic_id)
    print(bot_info.premium_id)
    print(bot_info.picture_url)
    print(bot_info.chat_mode)
    print(bot_info.mark_as_read_mode)
    return 'bot_info test'

@app.route("/get_group_summary", methods=['GET'])
def get_group_summary():
    summary = line_bot_api.get_group_summary(TEST_GROUP_ID)
    print(summary.group_id)
    print(summary.group_name)
    print(summary.picture_url)
    return 'get_group_summary test'

@app.route("/get_group_member_ids", methods=['GET'])
def get_group_member_ids():
    member_ids_res = line_bot_api.get_group_member_ids(TEST_GROUP_ID)
    print(member_ids_res.member_ids)
    print(member_ids_res.next)
    return 'get_group_member_ids test'

@app.route("/get_group_members_count", methods=['GET'])
def get_group_members_count():
    geoup_count = line_bot_api.get_group_members_count(TEST_GROUP_ID)
    print(geoup_count)
    return 'get_group_members_count test'



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)

    # try:
    #     line_bot_api.push_message('<to>', TextSendMessage(text='Hello World!'))
    # except LineBotApiError as e:
    #     print(e)

    # line_bot_api.reply_message(reply_token, TextSendMessage(text='Hello World!'))
