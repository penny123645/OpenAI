from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    print("callback...1")
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    print("pretty_echo...2")
    pretty_text = None
    match event.message.text:
        case "你叫什麼名字":
            pretty_text = '我叫張包子'
        case "你爸爸是誰":
            pretty_text = '張張'
        case "你爸爸的好友是誰":
            pretty_text = '佳穎 龜龜 阿牛 滴罵ㄍㄨㄣ @ 朝朝'
        case "你阿嬤是誰":
            pretty_text = '寶月'
        case "有了包子會快樂嗎":
            pretty_text = '我應該是能給你帶來心靈上的喜悅'
        case "那性方面呢":
            pretty_text = '那要去找個女友了'
            
    if (pretty_text != None):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )
        print("pretty_text:",pretty_text)
        return

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
            
        print("event.message.text:",event.message.text)
        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        pretty_text = ''
        for i in event.message.text:
        
            pretty_text += i
            pretty_text += random.choice(pretty_note)
    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )
        
if __name__ == "__main__":
    app.run()