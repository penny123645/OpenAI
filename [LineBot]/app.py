from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, StickerMessage, StickerSendMessage, ConfirmTemplate, TemplateSendMessage, MessageAction, URIAction, LocationMessage
from linebot.models.send_messages import ImageSendMessage
import openai
import configparser

import random
import json

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
OpenAI_API_Key = config.get('OpenAI-bot', 'API_Key')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    print("callback...1")
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print("json_data:",json_data)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'    
    for event in json_data['events']:
        print(" Event type:",event['message']['type'])
        if event['message']['type'] == 'text':
            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                abort(400)
        elif event['message']['type']== 'image':
            print('image')
            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                abort(400)
        elif event['message']['type'] == 'video':
            print('video')
        elif event['message']['type'] == 'audio':
            print('audio')
        elif event['message']['type'] == 'location':
            print('location')
    

@handler.add(MessageEvent)
def handle_message(event):
    print("handle_message")
    #
    
    if (event.message.type == "text"):
        print('text')
        msg = event.message.text
        reply_message = ''
        if msg != 'hi ai:':
            openai.api_key = OpenAI_API_Key
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg,
                max_tokens=256,
                temperature=0.5,
            )
        reply_message = response["choices"][0]["text"].replace('\n','')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    elif (event.message.type == "image"):
        print('image')
        #SendImage = line_bot_api.get_message_content(event.message.id)
        #line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=2))
    elif (event.message.type == "video"):
        print('video')
    elif (event.message.type == "audio"):
        print('audio')
    elif (event.message.type == "location"):
        print('location')
    return
    if msg != 'hi ai:':
        openai.api_key = OpenAI_API_Key
        response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg,
                max_tokens=256,
                temperature=0.5,
                )
        reply_message = response["choices"][0]["text"].replace('\n','')
        print("ai:",reply_message)
    elif event.source.user_id != "1234567821345678":
        print("event.message.text:",event.message.text)
        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        for i in event.message.text:
        
            reply_message += i
            reply_message += random.choice(pretty_note)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )
    
# 學你說話
#@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    print("pretty_echo")
    msg = event.message.text
    reply_message = ''
    #ai_msg = msg[:6].lower()
    if msg != 'hi ai:':
        openai.api_key = OpenAI_API_Key
        response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg,
                max_tokens=256,
                temperature=0.5,
                )
        reply_message = response["choices"][0]["text"].replace('\n','')
        print("ai:",reply_message)
    elif event.source.user_id != "1234567821345678":
            
        print("event.message.text:",event.message.text)
        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        for i in event.message.text:
        
            reply_message += i
            reply_message += random.choice(pretty_note)
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )    
        
if __name__ == "__main__":
    app.run()