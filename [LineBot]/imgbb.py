#API Key:24e642a5b8584c9562bcd65758a2b159
import base64
import requests
import imgbbpy
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
imgbb_apiKey = config.get('imgbb', 'imgbb_apiKey')
print("imgbb_apiKey:",imgbb_apiKey)
Filelocation = './bow.png'
client = imgbbpy.SyncClient(imgbb_apiKey)
image = client.upload(file=Filelocation)
print(image.url)