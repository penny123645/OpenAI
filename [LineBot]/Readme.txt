Line ID:(https://developers.line.biz/console/)
penny.openai@gmail.com
@a1b2c3d4

OPEN AI (https://platform.openai.com/account/api-keys)
penny.openai@gmail.com
a1b2c3d4

Imgbb(https://api.imgbb.com/)
penny.openai@gmail.com
Welcomeqa1

ngrok(https://dashboard.ngrok.com/settings)
penny.openai@gmail.com

-----------------------------
1. 設定 config.ini =>
2. 執行 python app.py
3. ngrok http 5000
4. 複製ngrok's URL, 設定Line Webhook settings (記得後面參數要帶"callback")
   e.g: https://4a7e-2001-b011-7806-9fe5-4cef-66e0-fa0b-826c.jp.ngrok.io/callback
5. 圖片上傳使用imgbb=>api key確認無誤 https://api.imgbb.com/ , "C:\[Work]\[openAI]\[LineBot]\imgbb.py"