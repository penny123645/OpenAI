#請CHAT gpt畫一張圖
from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage, ConfirmTemplate, TemplateSendMessage, MessageAction, URIAction, LocationMessage
from linebot.models.send_messages import ImageSendMessage
from base64 import b64decode
import os
import openai
import configparser
import random
import json
import imgbbpy
from datetime import datetime
import time

IMG_PATH = "./images/"

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
OpenAI_API_Key = config.get('OpenAI-bot', 'API_Key')

Img_Url = ""

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
    print("handle_message:",event.message.type)
    openai.api_key = OpenAI_API_Key
    if (event.message.type == "text"):
        print('text')
        msg = event.message.text
        if "幫我畫" in msg: 
            prompt_msg = msg
            file_name = generateImage_AndSave(prompt_msg, image_count=1) 
            imr_url = getImgurl(file_name)
            image_message = ImageSendMessage(
                original_content_url=imr_url,
                preview_image_url=imr_url
            )
            line_bot_api.reply_message(event.reply_token,image_message)
        else:
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
        # 將接到的圖存起來，回傳圖片URL
        message_content = line_bot_api.get_message_content(event.message.id)
        uid = getUID()
        savefile = uid+'.jpg'
        imr_url = ""
        filelocation = IMG_PATH+savefile
        with open(filelocation, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        time.sleep(2)
        print("filelocation:",filelocation)
        imr_url = getImgurl(filelocation)        
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=imr_url)
        )
    elif (event.message.type == "sticker"):
        print('sticker')
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

#請OPEN AI畫圖，存在Local
def generateImage_AndSave(prompt, image_count):
    print("generateImage_AndSave.....")
    img_local = ""
    images = []
    response = openai.Image.create(
        prompt=prompt,
        n=image_count,
        size='512x512',
        response_format='b64_json'
    )
    for image in response['data']:
        images.append(image.b64_json)
        
    #prefix = 'Img'
    prefix = getUID()
    for index,image in enumerate(images):
        img_local = IMG_PATH+f'{prefix}_{index}.jpg'
        print("img_local:",img_local)
        with open(img_local,'wb') as file:
            file.write(b64decode(image))
    return img_local

#將本地圖片上傳到imgbb，回傳圖片URL
def getImgurl(Filelocation):
    config = configparser.ConfigParser()
    config.read('config.ini')
    imgbb_apiKey = config.get('imgbb', 'imgbb_apiKey')
    client = imgbbpy.SyncClient(imgbb_apiKey)
    image = client.upload(file=Filelocation)
    print(image.url)
    return image.url
    
#取得唯一碼
def getUID():
    t = datetime.now().strftime('%Y%m%d%H%M%S%f')
    return t
    
if __name__ == "__main__":
    app.run()