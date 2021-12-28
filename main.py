from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FlexSendMessage
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
        content = {
            "type": "template",
            "altText": "this is a buttons template",
            "template": {
                "type":
                "buttons",
                "imageAspectRatio":
                "rectangle",
                "imageSize":
                "contain",
                "imageBackgroundColor":
                "#2B3CCA",
                "title":
                "按我啊",
                "text":
                "有種按我",
                "actions": [{
                    "type": "datetimepicker",
                    "label": "動作 1",
                    "data": "資料 1",
                    "mode": "datetime",
                    "initial": "2021-12-28T21:34",
                    "max": "2022-12-28T21:34",
                    "min": "2020-12-28T21:34"
                }]
            }
        }
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                  "type": "carousel",
                  "contents": [
                    {
                      "type": "bubble",
                      "size": "micro",
                      "hero": {
                        "type": "image",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip10.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "320:213"
                      },
                      "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "Brown Cafe",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                              },
                              {
                                "type": "text",
                                "text": "4.0",
                                "size": "xs",
                                "color": "#8c8c8c",
                                "margin": "md",
                                "flex": 0
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                  {
                                    "type": "text",
                                    "text": "東京旅行",
                                    "wrap": True,
                                    "color": "#8c8c8c",
                                    "size": "xs",
                                    "flex": 5
                                  }
                                ]
                              }
                            ]
                          }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                      }
                    },
                    {
                      "type": "bubble",
                      "size": "micro",
                      "hero": {
                        "type": "image",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip11.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "320:213"
                      },
                      "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "Brow&Cony's Restaurant",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                              },
                              {
                                "type": "text",
                                "text": "4.0",
                                "size": "sm",
                                "color": "#8c8c8c",
                                "margin": "md",
                                "flex": 0
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                  {
                                    "type": "text",
                                    "text": "東京旅行",
                                    "wrap": True,
                                    "color": "#8c8c8c",
                                    "size": "xs",
                                    "flex": 5
                                  }
                                ]
                              }
                            ]
                          }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                      }
                    },
                    {
                      "type": "bubble",
                      "size": "micro",
                      "hero": {
                        "type": "image",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip12.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "320:213"
                      },
                      "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "Tata",
                            "weight": "bold",
                            "size": "sm"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                              },
                              {
                                "type": "icon",
                                "size": "xs",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                              },
                              {
                                "type": "text",
                                "text": "4.0",
                                "size": "sm",
                                "color": "#8c8c8c",
                                "margin": "md",
                                "flex": 0
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                  {
                                    "type": "text",
                                    "text": "東京旅行",
                                    "wrap": True,
                                    "color": "#8c8c8c",
                                    "size": "xs",
                                    "flex": 5
                                  }
                                ]
                              }
                            ]
                          }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                      }
                    }
                  ]
                }
        )
        line_bot_api.reply_message(event.reply_token, flex_message )
    elif in_text == 'broadcast':
        line_bot_api.broadcast(TextSendMessage(text='Hello World!'))
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
