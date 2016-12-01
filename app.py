# encoding: utf-8
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

handler = WebhookHandler('Your_Channel_Secret') 
line_bot_api = LineBotApi('Your_Channel_Access_Token') 


@app.route('/')
def index():
    return "<p>Hello World!</p>"

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
        abort(400)

    return 'OK'

# ================= 機器人區塊 Start =================
# 自定義函式(Function) Start =================
import random
def lunch_choice():
    _choice = ["肥前屋","切仔麵","米粉湯","地下街","鐵板燒"]
    index = random.randint(0,len(_choice)-1)
    return _choice[index]

def is_my_word(msg,_word_list):
    is_word = False
    for i in _word_list:  
        if i in msg:     
            is_word = True
    return is_word

# 自定義函式(Function) End =================

@handler.add(MessageEvent, message=TextMessage)  # default
def handle_text_message(event):                  # default
    msg = event.message.text #message from user

    # 針對使用者各種訊息的回覆 Start =========
    _chg_word = ["換一個","不喜歡","吃過了"]
    
    if is_my_word(msg,_chg_word):
        choice = lunch_choice()
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="建議你可以吃「{}」".format(choice)))
    
    elif msg == "bye":
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="希望你有個愉快的午餐"))

    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="我聽不懂你在說什麼！"))

    # 針對使用者各種訊息的回覆 End =========

# ================= 機器人區塊 End =================

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
