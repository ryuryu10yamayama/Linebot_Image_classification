#Linebot用

import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage, FollowEvent
)
import numpy as np
import pya3rt
from keras.models import Sequential, load_model
from keras.preprocessing import image
import tensorflow as tf
import errno
import tempfile

app = Flask(__name__)

line_bot_api = LineBotApi(
    'vlK5lo2iprUJQ6JpByOcEryl6IRUmhej9Rs5rIuWt/PIvgZXEOaxNrDP7vDjHmEUo2zOJDCQNFIQNHiTQSlj+imBDXdPD9PHJQG7QDyDmtacsuh9qWbVoZEfsrDJZjaLQqHmMaFUGT8TWF3vUvnqAQdB04t89/1O/w1cDnyilFU=')  # アクセストークンを入れてください
handler = WebhookHandler('65a2e14ea12e45eac75110e86bcfa75d')  # Channel Secretを入れてください


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

    #テキストメッセージが送信されたときの処理


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    push_text = event.message.text

    #好きな女の子に関して(先頭へ)
    if (("好き"in push_text)or("すき"in push_text)or("好み"in push_text)) and (("女"in push_text)or("おんな"in push_text)or("メス"in push_text)or("おんなのこ"in push_text)or("女の子"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="かなこちゃん一筋だよ"))
    #好きな男の子に関して(先頭へ)
    elif (("好き"in push_text)or("すき"in push_text)or("好み"in push_text)) and (("男"in push_text)or("おとこ"in push_text)or("オス"in push_text)or("おとこのこ"in push_text)or("男の子"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ぼくはリラックマくんと仲良しだよ"))
    #食べ物に関して(先頭へ)
    elif (("好き"in push_text)or("すき"in push_text))and(("たべもの"in push_text)or("食べ物"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ぼくははちみつが大好物なんだ！"))
    #食べ物に関して(先頭へ)
    elif (("きらい"in push_text)or("嫌い"in push_text))and(("たべもの"in push_text)or("食べ物"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ピーマンが大嫌いなんだ！！"))
     #彼女はいる？
    elif (("彼女"in push_text)or("おんな"in push_text)or("女"in push_text))and(("いる"in push_text)or("居る"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="かなこちゃんだよ！(照)"))
    #昨日は寝られた？
    elif (("寝"in push_text))and(("きのう"in push_text)or("昨日"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ゆめボーイだからいつも睡眠不足なんだ。"))
    #昨日の食事
    elif (("食"in push_text)or("たべ"in push_text))and(("きのう"in push_text)or("昨日"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="昨日ははちみつドリアを食べたよ"))
    #かなこ
    elif (("かなこ"in push_text)or("彼女"in push_text)or("かのじょ"in push_text))and(("どんな"in push_text)or("かわいい"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="とってもかわいいんだよ！！！！！"))
     #かなこといつから付き合っているの
    elif (("かなこ"in push_text)or("彼女"in push_text)or("かのじょ"in push_text))and(("いつから"in push_text)or("どのくらい"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="産まれたときにはもう付き合っていたよ(照)"))
      #ひな
    elif (("ひな"in push_text)or("友達"in push_text)or("ともだち"in push_text))and(("どんな"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="とってもわんぱくなんだ！"))
    #今日の食事
    elif (("食"in push_text)or("たべ"in push_text))and(("きょう"in push_text)or("今日"in push_text)or("ひる"in push_text)or("昼"in push_text)or("よる"in push_text)or("夜"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="今日もはちみつドリアを食べたいなあ"))
    #年齢に関して
    elif (("何歳"in push_text) or ("なんさい"in push_text) or ("いくつ"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ぼくはまだ産まれたばかりの１才だよ。"))
    #性別に関して
    elif (("男の子"in push_text) or ("おとこ"in push_text) or ("男"in push_text) or ("おとこのこ"in push_text) or ("おんな"in push_text) or ("女"in push_text) or("女の子"in push_text) or ("おんなのこ"in push_text) or ("性別"in push_text) or ("雄"in push_text) or ("雌"in push_text) or ("オス"in push_text) or ("メス"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ぼくはオスのくまだよ。"))
    #すきなことに関して
    elif (("好きなこと"in push_text) or ("すきなこと"in push_text) or ("好きなもの"in push_text) or ("すきなもの"in push_text)or ("趣味"in push_text)):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text="ぼくははちみつをおなかいっぱい食べることが好きだなあ"))
    #得意なことに関して
    elif (("得意"in push_text) or ("とくい"in push_text) or ("上手"in push_text)or("できる"in push_text)):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text="ぼくはもらった画像から似ている動物を見つけるのが得意だよ"))
    # 友達に関して
    elif (("友達"in push_text)or("ともだち"in push_text)or("友人"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ぼくは最近ひなちゃんと友達になったんだ！"))
    #住んでいる場所に関して
    elif (("住"in push_text)or("すんでいる"in push_text)or("住んでいる"in push_text)or("すんでる"in push_text)or("住んでる"in push_text)or("出身"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ぼくはくーまの森に住んでいるよ"))
       #家族
    elif (("家族"in push_text)or("かぞく"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="パパとママと３人で暮らしているよ"))
       #ぱぱ
    elif (("パパ"in push_text)or("ぱぱ"in push_text)or("お父さん"in push_text)or("おとうさん"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="りゅうぱぱっていうんだ！いつも遊んでくれるよ！"))
       #ママ
    elif (("ママ"in push_text)or("まま"in push_text)or("お母さん"in push_text)or("おかあさん"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="とってもやさしいんだ！"))
       #姉妹
    elif (("姉妹"in push_text)or("兄弟"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="兄弟はいないんだ。"))
       #くーまの森
    elif (("くーまの森"in push_text)or("くーまのもり"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="とてもきれいなところだよ"))
       #遊び
    elif (("あそび"in push_text)or("遊"in push_text)or("あそぶ"in push_text)):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="ボール投げをよくしているよ"))
       #じゃんけん
    elif ("じゃんけん"in push_text)or("ジャンケン"in push_text):
        num = np.random.randint(0, 4)
        if num == 0:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="グー"))
        elif num == 1:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="チョキ"))
        elif num == 2:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="パー"))
        else:
           line_bot_api.reply_message(
               event.reply_token, TextSendMessage(text="必殺！！ブラックホール！！！"))
    else:
        reply_text = talkapi_response(push_text)  # talkapi_response関数にかける
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_text))


def talkapi_response(text):  # talkapiの実装部分
    apikey = "DZZoRRQa1aX11lr7W4bmpulm4tQmmJCK"
    client = pya3rt.TalkClient(apikey)
    response = client.talk(text)
    return ((response['results'])[0])['reply']


    #画像メッセージが送信されたときの処理
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
try:
    os.makedirs(static_tmp_path)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
        pass
    else:
        raise

graph = tf.get_default_graph()  # kerasのバグでこのコードが必要.
model = None
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):

    global model
    if model is None:
        model = load_model("./static/linebot_model.h5")

    global graph
    with graph.as_default():
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix="jpg" + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
                tempfile_path = tf.name#ファイルが保存された場所を示す

        dist_path = tempfile_path + '.' + "jpg"
        dist_name = os.path.basename(dist_path)#file名だけを抽出してくる
        os.rename(tempfile_path, dist_path)



        # ユーザから送信された画像のパスが格納されている
        filepath = os.path.join('./static', 'tmp', dist_name)
        
        class_label = ["熊", "猫", "鹿", "犬", "象", "蛙", "キリン", "ゴリラ","馬","ライオン","猿","ウサギ", "アザラシ"]
        img = image.load_img(filepath, target_size=(150,150))# 送信された画像を読み込み、リサイズする
        img = image.img_to_array(img)  # 画像データをndarrayに変換する
        #img = np.array(img)
        #img = (img-img.mean()) / img.std()
        # モデルは4次元データを受け取るのでnp.array()にimgをリストとして渡し、4次元のデータにする
        data = np.array([img])
        result = model.predict(data)
        predicted = result.argmax()
        pred_answer = "この写真は" + class_label[predicted] + "に似ているね！また一つ動物博士に近づいたよ！"

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=pred_answer))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3333))
    app.run(host='0.0.0.0', port=port)
